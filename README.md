# Package Minimalist

Find unused packages on this (Debian-based) Linux host so that you can remove them. Use dependencies to judge which packages are unused.

## Running

```
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate
python ./package-min.py
deactivate
```
