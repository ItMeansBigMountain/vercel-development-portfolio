#!/usr/bin/env python3
import importlib.util, shutil
bins = ['google-chrome','google-chrome-stable','chromium','chromium-browser','firefox']
print('BROWSERS:' + ','.join(f'{b}={bool(shutil.which(b))}' for b in bins))
print('LIBS:' + ','.join(f'{m}={bool(importlib.util.find_spec(m))}' for m in ['playwright','selenium','pyppeteer']))
