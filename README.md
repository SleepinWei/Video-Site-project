# Website
This repo is the project for "Foundations of Computer Science".   
Desired domain name: **SaBiSaBi.com**   
Finished on Dec.12. :star2:
# Group members  
Special thanks to my dear teammates! 🎉
+ zyw [@SleepinWei](https://github.com/SleepinWei)
+ lph [@lphlch](https://github.com/lphlch)
+ zxy [@HiziQ](https://github.com/HiziQ)
+ lmq [@lmqqqqqq](https://github.com/lmqqqqqq)
+ wwx [@qwqOscar](https://github.com/qwqOscar)
+ wxr [@wxrlalala](https://github.com/wxrlalala)
+ wtc [@TonyBest318](https://github.com/TonyBest318)
## division of work 
+ zyw   
  danmaku system: front-end 
+ lph 
  manager of front-end, user-homepage
+ zxy  
  video-play :front-end 
+ lmq     
  website homepage & login page 
+ wwx   
  manager of back-end 
+ wtc   
  login system : back-end,etc. 
+ wxr   
  danmaku system: back-end,etc. 
## Plan
front-end 
- [x] homepage 
- [x] user's personal homepage 
- [x] video page 
- [x] better nav bars 
- [x] better homepage design 
- ~~[ ] danmuku~~

back-end 
- [x] login & auth 
- [x] email sys 
- [x] migrations 
- ~~[ ] load danmuku~~
- [x] views.py (add db operations) 

## Get started 
Our website is based on flask and is managed with flask CLI.   
Launch the web using `flask run` command   
env settings are stored in `.env` file   
require `dotenv` package to set Environement variables.   

## Structure
website
+   **app**
    +   **auth**:all registration related functions are stored here(login,logout etc)
        +   views.py
        +   forms.py
    +   **main**
        +   errors.py: error handlers
        +   forms.py: web forms
        +   views.py: setting routers
    +   **static** 
        +   css 
        +   js 
        +   images 
        +   fonts 
        +   etc. 
    +   **templates**
        +   **auth**:store all registration related templates(current templates are just for tests) 
        +   some html templates here
    +   models.py: database models
+   **migrations**:for database migration 
+   **venv**
+   manager.py: manage app using flask-script 
