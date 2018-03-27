ECHO %0, %1, %2

SET start_ptr=%1
SET end_ptr=%2
SET delta=%3

ECHO start_ptr = %start_ptr%, end_ptr = %end_ptr%, delta = %delta%

for /l %%x in (%start_ptr%, -%delta%, %end_ptr%) do (
	ECHO %%x
	SET t="%%X"
	ECHO %t%
	SET /a y="%t%-2"
	ECHO %y%
	rem IF [%y%] LSS %end_ptr% SET y=%end_ptr%

	ECHO %%x %y%
	rem python getWeatherThenInsert2SQL.py %%x %y%
)
ECHO %y%

