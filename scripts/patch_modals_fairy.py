# -*- coding: utf-8 -*-
with open('frontend/src/components/CharacterCreationModal.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('sm:grid-cols-7', 'sm:grid-cols-8')
c = c.replace(".replace('Phần Thiên ', '')", ".replace('Phần Thiên ', '').replace('Bích Lạc ', '')")

with open('frontend/src/components/CharacterCreationModal.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('Patched CharacterCreationModal.tsx!')

with open('frontend/src/components/StatusModal.tsx', 'r', encoding='utf-8') as f:
    c2 = f.read()

c2 = c2.replace('sm:grid-cols-7', 'sm:grid-cols-8')
c2 = c2.replace(".replace('Phần Thiên ', '')", ".replace('Phần Thiên ', '').replace('Bích Lạc ', '')")

with open('frontend/src/components/StatusModal.tsx', 'w', encoding='utf-8') as f:
    f.write(c2)
print('Patched StatusModal.tsx!')
