# Identifying Logging Practices in Open Source Microservices Projects

Nowadays, most software projects have migrated from the old monolithic to microservice architectures.
Although this system architecture is now quite popular, there are not many studies that describe how observability practices are being employed.
Knowing that good observability leads to a better project development through the DevOps cycle and that logging is the most straightforward practice among the observability pillars, it is interesting to know its current adoption level and common practices.

In this empirical study, our goal is to understand what is the adoption level of observability by trying to identify popular logging practices in the open source community.
In order to achieve our goal, we mined over 10,000 open source Python repositories from GitHub.
Our analysis began after filtering down those previously mentioned to over 1,000 repositories which had at leats one Docker artifact in the project and was importing at least one known Python logging library.

These are our main research questions:
- **(RQ1)** How are containerized apps being logged?
- **(RQ2)** What kind of events are logged?
- **(RQ3)** What is the frequency of MSA projects adopting observability?


## Alunos integrantes da equipe

* Marco Túlio Resende Zuquim Alves

## Professores responsáveis

* José Laerte Pires Xavier Junior (orientador de conteúdo de TCCI)
* Lesandro Ponciano dos Santos (orientador acadêmico de TCCI)
* Hugo Bastos de Paula (orientador de TCCII)
