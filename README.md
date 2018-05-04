Efficiently Characterizing the Undefined Requests of a Rule-Based System (online)
=======

Introduction
------
Rule-based systems are used to define complex policies in several contexts, because of the flexibility and modularity they provide. 
This is especially critical for security systems, which may require to compose evolving policies for privacy, accountability, access control, etc. 
The inclusion of conflicting rules in complex policies, results in the inability of the system to unambiguously answer to certain requests, with possibly unpredictable effects. The static identification of these undefined requests is particularly challenging for unconstrained rule-based systems, including quantifiers, computations and chaining of rules. 

In this work, we introduce a static method to precisely characterize the set of all undefined requests for a given unconstrained rule-based system, providing the user with a global view of the rule conflicts. We propose an enumerative approach, made usable in practice by two key performance optimizations: a finer classification of the rules and the resort of the topological sorting. 
We demonstrate its application on a well-known policy with more than fifty rules.
This repository contains the artifacts used in this work.


Requirements
------
* Python v.3 
* Z3 v.4.6
* Z3py

How to use
------
SEE *fr.imt.naomod.acp/TESTS/iterative/testPerson.py* for example

Repository structure
------
* *src* contains the artifacts of our source code.
* *TESTS* contains the artifacts  used for our evaluation.


Contacts
------
> Zheng Cheng: zheng.cheng@imt-atlantique.fr 

> Jean-Claude Royer: jean-claude.royer@imt-atlantique.fr 

> Massimo Tisi: massimo.tisi@imt-atlantique.fr 
