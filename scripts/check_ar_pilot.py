#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/content/ar/pages/pilot.html'
OUTPUT = ROOT / 'dist/ar/pilot/index.html'
MANIFEST = ROOT / 'docs/i18n/ar-translation-manifest.json'

errors: list[str] = []
source = SOURCE.read_text(encoding='utf-8')
output = OUTPUT.read_text(encoding='utf-8')

reviewed_phrases = [
    'المشروع التجريبي للعُقدة لمدة 60 يومًا',
    'من التصوّر إلى عُقدة عاملة.',
    'مشروع محدود النطاق يتضمن تركيب جهاز مناسب، وربط سير عمل مفيد، وتحديد حدود الثقة، وتوفير أدلة قابلة للفحص.',
    'محدودة بما يكفي لإنجازها، وحقيقية بما يكفي لتُحدث أثرًا.',
    'خمس مراحل. سجل واحد متواصل.',
    'الأيام من 1 إلى 7',
    'الأيام من 8 إلى 21',
    'الأيام من 22 إلى 32',
    'الأيام من 33 إلى 52',
    'الأيام من 53 إلى 60',
    'الاختبار والتحقق',
    'ما الذي يستلمه العميل؟',
    'ما مواصفات سير العمل الأول المناسب؟',
    'ما الذي لا ينبغي أن يبدأ به المشروع التجريبي؟',
    'المسار التجاري والأسعار',
    'اعرض علينا سير العمل الذي لا يحتمل فقدان سياقه.',
]

for phrase in reviewed_phrases:
    if phrase not in source or phrase not in output:
        errors.append(f'ar/pilot: reviewed phrase missing from source or generated output: {phrase}')

superseded_phrases = [
    'تجربة العقدة خلال 60 يوماً',
    'من الإمكان إلى عقدة عاملة.',
    'ارتباط محدود',
    'حقيقية بما يكفي لتهم',
    'سجل متصل واحد',
    '<span>1–7</span>',
    '<span>8–21</span>',
    '<span>22–32</span>',
    '<span>33–52</span>',
    '<span>53–60</span>',
    'التوقف النظيف',
    'أصغر عقدة صادقة',
]

for phrase in superseded_phrases:
    if phrase in source or phrase in output:
        errors.append(f'ar/pilot: superseded wording remains: {phrase}')

required_sections = [
    'deliverables-section',
    'pilot-fit-grid',
    'pilot-pricing-grid',
]
for marker in required_sections:
    if marker not in source or marker not in output:
        errors.append(f'ar/pilot: required English-equivalent section missing: {marker}')

price_numbers = ('5,400', '400', '10,750', '750', '30,000', '2,500')
for number in price_numbers:
    marker = f'<bdi dir="ltr">{number}</bdi>'
    if marker not in source or marker not in output:
        errors.append(f'ar/pilot: price number is not bidi-isolated: {number}')

manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
reviewed_routes = manifest.get('reviewed_routes', [])
pending_routes = manifest.get('pending_routes', [])
if '/ar/pilot/' not in reviewed_routes or '/ar/pilot/' in pending_routes:
    errors.append('ar/pilot: manifest reviewed/pending route state is incorrect')
if manifest.get('human_reviewed') is not False:
    errors.append('ar: partial route review must not mark the full locale human reviewed')

if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)

print('PASS: Arabic Pilot human-reviewed wording, RTL day ranges, source completeness, and price formatting')
