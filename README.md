### 1DV607 --- Object-Oriented Analysis and Design

Workshop Assignments
=======================================================================
*Copyright(c) 2017 Jonas Sjöberg*  
<https://github.com/jonasjberg>  
<http://www.jonasjberg.com>  
University mail: `js224eh[a]student.lnu.se`  

--------------------------------------------------------------------------------

Workshops assignments for the course "`1DV607` -- "Object-Oriented Analysis and
Design", given at [Linnaeus University](https://lnu.se/en/) as part of the
"[Software Development and Operations](https://udm-devops.se/)" programme.

Written by Jonas Sjöberg.



Workshop 1 --- Domain Modeling
==============================


Version #1 (peer reviewed)
--------------------------

* [PDF Document](https://github.com/jonasjberg/1dv607_workshops/raw/master/workshop1/release/js224eh_version-1-peer-reviewed.pdf)
* [LaTeX Sources (`.zip`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop1_anon.zip)


Version #2 (FINAL)
------------------

* [PDF Document](https://github.com/jonasjberg/1dv607_workshops/raw/master/workshop1/release/js224eh_version-2-final.pdf)
* [LaTeX Sources (`.zip`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop1-final-submission.zip)
* [LaTeX Sources (`.tar.gz`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop1-final-submission.tar.gz)



Workshop 2 --- Design
=====================
Application implementation written in Python.


Version #1 (peer reviewed)
--------------------------

* [Stand-alone Windows Executable](https://github.com/jonasjberg/1dv607_workshops/raw/master/workshop2/build/jollypirate.exe)
* [Python Sources (`.zip`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop2-peer-review-submission.zip)
* [Python Sources (`.tar.gz`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop2-peer-review-submission.tar.gz)


Version #2 (FINAL)
------------------

* [Class Diagram (`.png`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission/workshop2/uml/class-diagram.png)
* [Class Diagram (`.eps`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission/workshop2/uml/class-diagram.eps)
* [Sequence Diagram - List all Members (`.png`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission/workshop2/uml/seq_list-all-members.png)
* [Sequence Diagram - List all Members (`.eps`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission/workshop2/uml/seq_list-all-members.eps)
* [Sequence Diagram - Register Member (`.png`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission/workshop2/uml/seq_register-member.png)
* [Sequence Diagram - Register Member (`.eps`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission/workshop2/uml/seq_register-member.eps)
* [Stand-alone MacOS/OSX Executable](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission/workshop2/build/jollypirate_osx)
* [Stand-alone Linux Executable](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission/workshop2/build/jollypirate_linux)
* [Stand-alone Windows Executable](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission/workshop2/build/jollypirate_win.exe)
* [Python and Diagram Sources (`.zip`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop2-final-submission.zip)
* [Python and Diagram Sources (`.tar.gz`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop2-final-submission.tar.gz)


Version #3 (FINAL with FIXES)
-----------------------------

* [Class Diagram (`.png`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission-fixes/workshop2/uml/class-diagram.png)
* [Class Diagram (`.eps`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission-fixes/workshop2/uml/class-diagram.eps)
* [Sequence Diagram - List all Members (`.png`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission-fixes/workshop2/uml/seq_list-all-members.png)
* [Sequence Diagram - List all Members (`.eps`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission-fixes/workshop2/uml/seq_list-all-members.eps)
* [Sequence Diagram - Register Member (`.png`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission-fixes/workshop2/uml/seq_register-member.png)
* [Sequence Diagram - Register Member (`.eps`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission-fixes/workshop2/uml/seq_register-member.eps)
* [Stand-alone MacOS/OSX Executable](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission-fixes/workshop2/build/jollypirate_osx)
* [Stand-alone Linux Executable](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission-fixes/workshop2/build/jollypirate_linux)
* [Stand-alone Windows Executable](https://github.com/jonasjberg/1dv607_workshops/raw/workshop2-final-submission-fixes/workshop2/build/jollypirate_win.exe)
* [Python and Diagram Sources (`.zip`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop2-final-submission-fixes.zip)
* [Python and Diagram Sources (`.tar.gz`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop2-final-submission-fixes.tar.gz)


### Changes

* __Update the class diagram__
* __Remove string formatting from the model__  
  Removes string formatting property `Member.name_full` from the Member model,
  from received feedback on the final version.
* __Fix inconsistent member IDs__  
    As pointed out in the feedback to the final submission of this project, the
    Member ID implementation was flawed in that it returned different IDs for
    each program run.

    This was due to using `Member.__hash__()` to generate the IDs.
    The method uses a different randomized seed for each execution.

    From the Python 3 documentation>

    > Hash randomisation is turned on by default in Python 3.
    > This is a security feature:
    > Hash randomization is intended to provide protection against a
    > denial-of-service caused by carefully-chosen inputs that exploit
    > the worst case performance of a dict construction

    This method should not be used for IDs that should be consistent across
    program execution runs, serialization, etc.

    This commit fixes this by instead calculating a MD5 sum of the same
    three (arbitrarily chosen) attributes as before.


Workshop 3 --- Design Using Patterns
====================================
Refactoring and modifications of an exiting Java application.


Version #1 (FINAL)
------------------

* [Class Diagram (`.png`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop3-final-submission/workshop3/uml/class-diagram_modified.png)
* [Class Diagram (`.eps`)](https://github.com/jonasjberg/1dv607_workshops/raw/workshop3-final-submission/workshop3/uml/class-diagram_modified.eps)
* [Stand-alone cross-platform Executable (`.zip`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop3-final-submission.zip)
* [Stand-alone cross-platform Executable (`.tar.gz`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop3-final-submission.tar.gz)
* [Java and Diagram Sources (`.zip`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop3-final-submission.zip)
* [Java and Diagram Sources (`.tar.gz`)](https://github.com/jonasjberg/1dv607_workshops/archive/workshop3-final-submission.tar.gz)
