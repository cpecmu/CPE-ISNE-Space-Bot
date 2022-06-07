import role_ids


welcome_message = '''Welcome to **CPE-ISNE Space** ,<@{}>! Please check out the <#{}>. Glad to have you here!'''

welcome_message_dm = '''Welcome to **CPE-ISNE Space** ,<@{}>! Please answer these questions to verify yourself.
'''

verify_question_0 = '''
**Question 0: **

What is your student ID?
โปรดระบุรหัสนักศึกษาของคุณ

(Answer in number)

'''

verify_invalid_0_0 = '''
The student ID you entered is incorrect. Please check and try again.

'''

verify_question_cpe_0 = '''
**Question 0.5: **

Are you currently a cpe student?
คุณเป็นนักศึกษาในหลักสูตร CPE ใช่หรือไม่?

(y/n)

'''

verify_question_isne_0 = '''
**Question 0.5: **

Are you currently a isne student?
คุณเป็นนักศึกษาในหลักสูตร ISNE ใช่หรือไม่?

(y/n)

'''

verify_question_isne_0 = '''
**Question 0.5: **

Are you an alumni (or already graduated bachalor's degree)? 
คุณเป็นศิษย์เก่า(หรือจบปริญญาตรีแล้ว)ใช่หรือไม่?

(y/n)

'''

verify_question_1 = '''
**Question 1: **

Which programming language do you use in Computer Programming, a class for year 1 student?
วิชา Computer Programming ที่เรียนในปี 1 ใช้ภาษาคอมพิวเตอร์ใดในการเรียน?

(ruby/pascal/java/c++/python/haskell/other)

'''

verify_question_2 = '''
**Question 2: **

Which floor of 30 years building is our major's administration section located?
ฝ่ายธุรการของภาควิชาอยู่ชั้นใดของตึก 30 ปี?

(Answer in number)

'''

verify_wrong_answer_tryagain = '''
Your answer is incorrect. Please try again.

'''

verified_message = '''
Verification finished!

You have been given the role: **{}**. 

If you've been given the wrong role, please contact any of our admins through direct message.

'''

role_message = '''Which do you consider yourself?

🔵 <@&{cpe}>
🟢 <@&{isne}> 
🟣 <@&{alumni}> 

Click to get you role(s)!'''.format(cpe = role_ids.cpe,isne = role_ids.isne, alumni = role_ids.alumni)