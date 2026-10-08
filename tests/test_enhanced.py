import builtins
from pathlib import Path
import pandas as pd
import pytest
from app.calculation_record import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import Caretaker
from app.calculator_repl import Calculator, main, HELP
from app.exceptions import CalculatorError, ConfigurationError, OperationError
from app.history import History
from app.input_validators import finite_number
from app.operations import OperationFactory

@pytest.fixture
def cfg(tmp_path):
    return CalculatorConfig(tmp_path / 'history.csv', True, 2)

@pytest.mark.parametrize('op,a,b,result', [('+',2,3,5),('add',2,3,5),('-',5,3,2),('subtract',5,3,2),('*',2,3,6),('multiply',2,3,6),('/',6,3,2),('divide',6,3,2),('^',2,3,8),('power',2,3,8),('root',25,2,5),('root',-27,3,-3),('root',-1,3,-1)])
def test_operations(op,a,b,result):
    assert Calculation.perform(op,a,b).result == pytest.approx(result)

@pytest.mark.parametrize('op,a,b', [('/',1,0),('root',1,0),('root',-4,2),('root',-4,2.5),('^',-4,.5),('^',1e200,3),('^',0,-1),('root',0,-1),('bad',1,2)])
def test_invalid_operations(op,a,b):
    with pytest.raises(CalculatorError):
        Calculation.perform(op,a,b)

@pytest.mark.parametrize('value', ['xyz','nan','inf',None])
def test_invalid_values(value):
    with pytest.raises(CalculatorError):
        finite_number(value)

def test_factory_type_invalid():
    with pytest.raises(OperationError):
        OperationFactory.create(None)

def test_config(monkeypatch, tmp_path):
    monkeypatch.setenv('CALC_HISTORY_FILE',str(tmp_path/'data.csv'))
    monkeypatch.setenv('CALC_MAX_HISTORY','4')
    monkeypatch.setenv('CALC_AUTO_SAVE','false')
    c=CalculatorConfig.from_env()
    assert c.max_history==4 and not c.auto_save
    for name,value in [('CALC_HISTORY_FILE',' '),('CALC_AUTO_SAVE','sometimes'),('CALC_MAX_HISTORY','bad'),('CALC_MAX_HISTORY','-1')]:
        monkeypatch.setenv(name,value)
        with pytest.raises(ConfigurationError): CalculatorConfig.from_env()
        monkeypatch.setenv(name, {'CALC_HISTORY_FILE':str(tmp_path/'data.csv'),'CALC_AUTO_SAVE':'false','CALC_MAX_HISTORY':'4'}[name])
    for name in ('CALC_HISTORY_FILE','CALC_AUTO_SAVE','CALC_MAX_HISTORY'): monkeypatch.delenv(name)
    assert CalculatorConfig.from_env().max_history==1000

def test_memento():
    m=Caretaker()
    assert m.undo([])==[] and m.redo([])==[]
    m.remember([])
    assert m.undo([1]) == []
    assert m.redo([])==[1]
    m.remember([2])
    assert m.redo([2])==[2]

def test_history_csv(tmp_path):
    h=History(2)
    r=Calculation.perform('+',1,2)
    for _ in range(3): h.append(r)
    assert len(h.entries)==2
    assert list(h.dataframe().columns)==['operation','a','b','result','timestamp']
    f=tmp_path/'nested'/'saved.csv'
    assert not h.load(f)
    h.save(f)
    j=History(); assert j.load(f)
    assert len(j.entries)==2 and j.entries[0].result==3
    h.clear(); assert len(h.entries)==0
    f.write_text('incorrect\n1\n')
    with pytest.raises(CalculatorError): j.load(f)
    f.write_text('')
    with pytest.raises(CalculatorError): j.load(f)
    f.write_text('operation,a,b,result,timestamp\n+,no,2,3,now\n')
    with pytest.raises(CalculatorError): j.load(f)
    with pytest.raises(CalculatorError): j.save(tmp_path/'nested')

def test_facade_and_observers(cfg):
    c=Calculator(cfg)
    assert c.calculate('+',1,2)==3
    assert cfg.history_file.is_file()
    assert c.calculate('-',5,1)==4
    assert c.calculate('*',2,3)==6
    assert len(c.history.entries)==2
    c.undo(); assert len(c.history.entries)==2
    c.redo(); assert len(c.history.entries)==2
    c.clear(); assert not c.history.entries
    c.undo(); assert len(c.history.entries)==2
    c.redo(); assert not c.history.entries
    assert c.load() and not c.history.entries
    assert Calculator(cfg).history.entries == []
    no=Calculator(CalculatorConfig(cfg.history_file,False,5),load_existing=False)
    no.calculate('+',3,4)
    no.clear(); no.undo(); no.redo()
    assert len(no.history.entries)==0
    missing=Calculator(CalculatorConfig(cfg.history_file.parent/'missing.csv',False,5))
    assert not missing.load()

def test_repl(monkeypatch,capsys,tmp_path):
    cfg=CalculatorConfig(tmp_path/'h.csv',True,5)
    monkeypatch.setattr('app.calculator_repl.CalculatorConfig.from_env',lambda:cfg)
    answers=iter(['help','+','2','3','history','undo','redo','save','clear','load','nonsense','1','2','exit'])
    monkeypatch.setattr(builtins,'input',lambda _:next(answers))
    main()
    out=capsys.readouterr().out
    assert 'Result: 5.0' in out and 'Unsupported operation' in out and HELP in out

def test_repl_missing_and_interrupt(monkeypatch,capsys,tmp_path):
    monkeypatch.setattr('app.calculator_repl.CalculatorConfig.from_env',lambda:CalculatorConfig(tmp_path/'absent.csv',False,5))
    answers=iter(['load','exit'])
    monkeypatch.setattr(builtins,'input',lambda _:next(answers))
    main(); assert 'No saved history' in capsys.readouterr().out
    def interrupted(_): raise EOFError()
    monkeypatch.setattr(builtins,'input',interrupted)
    main(); assert 'Goodbye' in capsys.readouterr().out

def test_repl_startup_error(monkeypatch,capsys):
    def broken(): raise ConfigurationError('bad')
    monkeypatch.setattr('app.calculator_repl.CalculatorConfig.from_env',broken)
    main(); assert 'Configuration/history error' in capsys.readouterr().out

def test_module_entrypoint(monkeypatch,tmp_path,capsys):
    import runpy
    monkeypatch.setattr('app.calculator_repl.CalculatorConfig.from_env',lambda:CalculatorConfig(tmp_path/'h.csv',False,5))
    monkeypatch.setattr(builtins,'input',lambda _: 'exit')
    runpy.run_module('app',run_name='__main__')
    assert 'Goodbye!' in capsys.readouterr().out

def test_importable_entrypoint():
    import app.__main__
    assert callable(app.__main__.main)
