@echo off
if "%1" == "lasts" goto checklasts
if "%1" == "errs" goto checkerrs

echo *******************
echo Test of last lines:
echo *******************

for %%f in (all-steps\*.log) do call %0 lasts %%f
for %%f in (automodel\*.log) do call %0 lasts %%f
for %%f in (commands\*.log) do call %0 lasts %%f
for %%f in (salign\*.log) do call %0 lasts %%f

echo ****************
echo Test of errors:
echo ****************

for %%f in (all-steps\*.log) do call %0 errs %%f
for %%f in (automodel\*.log) do call %0 errs %%f
for %%f in (commands\*.log) do call %0 errs %%f
for %%f in (salign\*.log) do call %0 errs %%f
goto end


:checkerrs
set file=%2
find "E>" %file% > nul
if errorlevel 1 goto end
find /N "E>" %file%
goto end


:checklasts
set file=%2
find "Total CPU time" %file% > nul
if not errorlevel 1 goto end
echo "FILE %file%"
goto end

:end
