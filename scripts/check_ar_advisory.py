#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/content/ar/pages/advisory.html'
OUTPUT = ROOT / 'dist/ar/advisory/index.html'
MANIFEST = ROOT / 'docs/i18n/ar-translation-manifest.json'
REVIEW = ROOT / 'docs/i18n/reviews/ar-advisory-2026-08-06-ali-khalil.md'

errors: list[str] = []
source = SOURCE.read_text(encoding='utf-8')
output = OUTPUT.read_text(encoding='utf-8')

required_phrases = [
    'حدّد ما يُعَدّ نجاحًا للذكاء الاصطناعي في مؤسستك قبل أن يحدده الآخرون نيابةً عنك',
    'نبدأ بالمهمة، لا بالنموذج.',
    'الغاية ليست المزيد من الذكاء الاصطناعي',
    'سلطة القرار',
    'قرار مؤسسي قابل للاستمرار، لا عرض شرائح آخر',
    'خدماتنا الاستشارية ليست وسيلة مقنّعة لبيع الأجهزة',
    'نؤطّر. نحدّد الحدود. نقرّر. نُثبت، ثم نواصل.',
    'قرارات مؤثرة، ومسؤول بشري واضح وخاضع للمساءلة',
    'القدرة على قول «لا» جزء من الخدمة.',
    'أخبرنا بما يجب أن يظل ثابتًا',
    'عُقدًا محلية',
    'إحدى عُقد QuietWire',
]

for phrase in required_phrases:
    if phrase not in source or phrase not in output:
        errors.append(f'ar/advisory: approved phrase missing from source or output: {phrase}')

superseded = [
    'حدّد معنى نجاح الذكاء الاصطناعي قبل أن يحدّده غيرك نيابةً عنك.',
    'الهدف ليس المزيد من الذكاء الاصطناعي.',
    'حكم مستقل',
    'تحديد الإطار. رسم الحدود. اتخاذ القرار. الاختبار والاستمرار.',
    'Arabic Advisory translation is under review.',
]

for phrase in superseded:
    if phrase in source or phrase in output:
        errors.append(f'ar/advisory: superseded wording remains: {phrase}')

if not REVIEW.is_file():
    errors.append('ar/advisory: missing review provenance record')
else:
    review_text = REVIEW.read_text(encoding='utf-8')
    for name in ('Ali Adnan', 'Khalil', 'Chris Blask'):
        if name not in review_text:
            errors.append(f'ar/advisory: review record does not name {name}')
    if 'approved for publication' not in review_text:
        errors.append('ar/advisory: review record does not contain publication approval')

manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
drafts = manifest.get('human_authored_drafts', [])
entry = next((item for item in drafts if item.get('route') == '/ar/advisory/'), None)
if entry is None:
    errors.append('ar/advisory: manifest does not record the human-authored page')
else:
    if entry.get('authors') != ['Ali Adnan', 'Khalil']:
        errors.append('ar/advisory: manifest authors are incorrect')
    if entry.get('status') != 'human_reviewed_and_approved_for_publication':
        errors.append('ar/advisory: manifest approval status is incorrect')
    if entry.get('language_approval') != 'Ali Adnan':
        errors.append('ar/advisory: language approval is not attributed to Ali Adnan')
    if entry.get('publication_approval') != 'Chris Blask':
        errors.append('ar/advisory: publication approval is not attributed to Chris Blask')

if '/ar/advisory/' not in manifest.get('reviewed_routes', []):
    errors.append('ar/advisory: route must be listed as reviewed after approval')
if '/ar/advisory/' in manifest.get('pending_routes', []):
    errors.append('ar/advisory: route must not remain pending after approval')
if manifest.get('human_reviewed') is not False:
    errors.append('ar: partial route review must not mark the full locale human reviewed')

if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)

print('PASS: Arabic Advisory approved wording, provenance, node diacritics, and publication state')
