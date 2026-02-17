# Week 2: Getting to grips with an unfamiliar system

In this lab we will familiarise ourselves with the following:

* Identifying potential target projects for your group project.
* Importing an unfamiliar system into our Git repository.
* Bottom-up comprehension:
  * Scanning through the repository code contents to identify potentially important concepts.
  * Using basic tools to examine important design constructs.

Although you have individual repositories, it is important that you work on this as a group. Ideally, you should end 
this project with a list of candidate projects that you can then focus on throughout the rest of this project.

## 1. Pick a potential project

* As a team, scan through the [candidate Python projects](https://docs.google.com/document/d/11W2wAbwMuW16jmeh2aXvBaDqz0rmNqyjMFzwAY4QGbw/edit?tab=t.0). Each team 
member should pick a different project.
  * Consider whether the project adheres to the eligibility conditions set out in the assignment brief.
* Go to the GitHub site for that project and download a snap-shot of the source code. 
  * You can do this by selecting the "<> Code" drop-down box in GitHub, and clicking on the "Download ZIP" option.
  * Do *not* use Git to check out
the project. You will be incorporating this project into your own git repository, and if you clone it with git, the underlying metadata will most likely raise unnecessary problems when you commit it to your personal GitHub Classroom repo.

## 2. Add the code snapshot to your GitHub repository for this lab

* If you have not done so already, clone your GitHub classroom lab repo for this week (it should contain this README file). You can use the built-in Git support in VS-Code to do this if you wish.
  * Set up a .venv environment, as you did in your last lab.
* Unpack the ZIP file you downloaded for your target project into a directory.
* Add this directory to your cloned GitHub directory.

## 3. Carry out a bottom-up analysis of the project.

Your broad aim should be to provide answers to the following questions:

1. What are the key functions of this system?
2. Which packages / directories within the system are particularly important?
3. Which particular classes are particularly important?
   * Are there key abstract classes, or classes that sit at the top of inheritance
   hierarchies?
   * Are there classes that look as though they are called often?
   * Obvious design patterns?
4. Are there any potential problematic aspects of design?
   * Code smells?
   * Violations of design principles?

For this process, it makes sense to start from a visual scan of the directory contents, skimming through some of the 
files. Then you can follow this up by using some of the tools we covered in the lecture.

To run pyreverse you will need to do the following steps:

1. Ensure that you have set up and activated your `.venv`.
    * This is what we covered in last week's lab.
2. Ensure that you have GraphViz installed, and that the `dot` command is on your path (i.e. you can run `dot` from your command line).
    * Follow the link to do this from the self-study materials section for this week on Blackboard.
3. Ensure that PyLint is installed: `pip install -U pylint`
  
    * This includes the pyreverse tool, which we'll be using.

4. Run `pyreverse` on the command line:

    * `pyreverse -o png -p [output_name_suffix] --ignore=[comma-separated list of directories to ignore] --filter-mode=PUB_ONLY --colorized [target_directory]`

So, for the CovaSim example, the command would look as follows: `pyreverse -o png -p covasim  --ignore=tests  --filter-mode=PUB_ONLY  --colorized ./covasim`

You can add more options. These are all listed by default if you just run `pyreverse` without any arguments.

## 4. Write up a set of notes and commit.

* Put your notes (ideally in [Markdown format](https://www.markdownguide.org/cheat-sheet/)) into a file called `notes.md` 
in the root directory of the project.
  * Note, the name of this file is important, because the lab tests will automatically check for the existence of this 
  file when you commit.

## 5. Share your thoughts with the group.

Amongst the projects selected by your group, is there a project that looks particularly suitable? 
Discuss the suitability of each project in turn (bearing in mind the eligibility rules set out in the assessment 
brief). 

If you believe that you have found a project that you like, then the sooner you pick it, the more likely you are to get 
it (two teams cannot pick the same project, and projects are allocated on a first-come-first-served basis).