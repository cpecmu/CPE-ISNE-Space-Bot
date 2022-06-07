import role_ids


welcome_message = '''Welcome to the **CPE-ISNE Space** ,<@{}>! Please check out the <#{}>. Glad to have you here!'''

welcome_message_dm = '''Welcome to the **CPE-ISNE Space** ,<@{}>! Please answer these questions to verify yourself.
'''

verify_question_1 = '''
**Question 1: **

Which programming language do you use in 261102 Computer Programming, a class for year 1 student?

วิชา 261102 Computer Programming ที่เรียนในปี 1 ใช้ภาษาคอมพิวเตอร์ใดในการเรียน?
'''

verify_question_2 = '''
**Question 2: **

According to your curriculum, which semester do you study 261102 Computer Programming?

ตามหลักสูตรของท่าน ท่านได้เรียนวิชา 261102 Computer Programming ในภาคเรียนใด?

(Answer in number)
'''

verified_message = "Verification finished! Please visit **#roles** channel in the server to get your role(s)."

role_message = '''Which do you consider yourself?

🔵 <@&{cpe}>
🟢 <@&{isne}> 
🟣 <@&{alumni}> 

Click to get you role(s)!'''.format(cpe = role_ids.cpe,isne = role_ids.isne, alumni = role_ids.alumni)