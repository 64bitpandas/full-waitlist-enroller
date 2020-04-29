# The Berkeley Full Waitlist Enroller

**Got a terrible enrollment time this semester? Tired of seeing the image below?**
(that is totally me lol)

![waitlist full noo](img/full.png)

This probably won't help since enrollment is a lost cause, but at least you can save some time having to take a few minutes of your time trying to add the class manually just to see that blue square of doom.

![blue square](img/bluesquare.png)

## How to Use

1. Install [Python 3](https://www.python.org/downloads/) and [Geckodriver](https://github.com/mozilla/geckodriver/releases).
2. Clone the repository: `git clone https://github.com/64bitpandas/full-waitlist-enroller`
3. Enter the directory: `cd full-waitlist-enroller`
4. Install requirements: `pip install -r requirements.txt`
5. Edit `constants.py` to add the class you want in `COURSE_NAME` and the swapped class in `SWAP_NAME`. Use the format in the swap menu.
    - Example swap: `MATH 110: LINEAR ALGEBRA`
    - Example course: `DATA C100-001 LEC (33470)`
5. Run using `python3 enroll.py` and hope for the best.
6. Repeat once a week/day/hour (for extra laziness just set a cronjob or something)


**By default, this script uses the SWAP feature to replace a class you are already enrolled in with the full class (if successful, haha good luck).** I'd suggest to enroll in a class that's open and you are willing to swap out if you haven't already.

## How does it work?

This script is inspired by [encadyma's caldining status checker](https://github.com/encadyma/dining_pts). It uses [Selenium](https://www.selenium.dev/) to automate button-clicking and page reading for you!

<!-- Insert more description -->

## FAQ

**There is a bug and/or it doesn't work with XX class?**
 - Create an [issue](https://github.com/64bitpandas/full-waitlist-enroller/issues) describing the problem and I'll probably ignore it.
 
**I ran this and it dropped me from all my classes. Who do I sue?**
 - Forward all legal inquiries to: <br>Supreme Court of the United States<br>1 First Street, NE Washington, DC<br>20543

**Did this help you get into your classes?**
 - No. No it did not.

**Was it even worth it to make this then???**
 - Yes.

**I have a question not on this FAQ?**
 - ok