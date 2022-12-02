# ReadWriteExecute
ReadWriteExecuteApp

Simple django app with a simple purpose of learning a japanese language. It will contain a dictionary with a search option where you can find english-japanese translation written in hiragana/katakana (and optional kanji where it applies).

## Requirements

Right now we are working on Django 4.0.6 in order to run the project, clone the repo, create virtual enviroment with

```
python -m venv .venv
```

and after activating it with the proper script (many IDEs do that automatically in a new terminal, more on the topic on https://docs.python.org/3/tutorial/venv.html) install the dependencies with

```
pip install -r requirements.txt
```

and you're good to go.

## Dictionary database creation

Right now database used internally is based on https://www.edrdg.org/jmdict/j_jmdict.html. In the future it will be imported to the production version with proper credits, as allowed by the **Usage of the Dictionary Files** described on http://www.edrdg.org.

Importing the dictionary uses django command

```
python manage.py importdictionary dictionary_file_name -cc
```

`dictionary_file_name` is expected to be a .json file with entries containing following data:
- `gloss` - english word/phrase
- `reb` - japanese translation written in hiragana/katakana
- `keb` - (optional) japanese translation written with kanji
