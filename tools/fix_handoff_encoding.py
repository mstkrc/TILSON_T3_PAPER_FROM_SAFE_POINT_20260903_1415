from pathlib import Path

path = Path('recovery/09_SESSION_HANDOFF.md')
text = path.read_bytes().decode('utf-8')
text = text.replace('\r\n', '\n').replace('\r', '\n').rstrip('\n')
note = ('\n\nFAZ-21 DÜZELTİCİ START GATE NOTU:\n'
        'Önceki Faz-21 OPEN GATE kabulü eksik sayılmıştır.\n'
        'Faz-21 IN_PROGRESS kaydı erken kabul edilmiş ve WAITING_CORRECTIVE_START_GATE olarak düzeltilmiştir.\n'
        'Anayasa 12. madde ve Faz-13 UI kayıtları özel olarak okunmuştur.\n'
        'Faz-21 uygulaması henüz başlamamıştır.\n'
        'Resmi START GATE 10/10 PASS ve kullanıcı onayı olmadan UI Operational Cockpit Review başlatılamaz.\n'
        'Kod değişikliği, UI code değişikliği, paper trade start, live trading ve gerçek emir endpoint’i yasaktır.\n'
        'LIVE_TRADING=false korunmuştur.')
if 'FAZ-21 DÜZELTİCİ START GATE NOTU:' not in text:
    text += note
path.write_text(text.rstrip('\n') + '\n', encoding='utf-8', newline='\n')
print('HANDOFF_UTF8_LF_FINAL_NEWLINE=PASS')
