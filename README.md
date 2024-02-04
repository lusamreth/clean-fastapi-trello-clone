# clean-fastapi-trello-clone


[![FastAPI](https://img.shields.io/badge/FastAPI-005572?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SqlAlchemy](https://img.shields.io/badge/FastAPI-005572?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAPI](https://img.shields.io/badge/openapi-6BA539?style=for-the-badge&logo=openapi-initiative&logoColor=fff)](https://www.openapis.org/)
[![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/)
[![Typed with: pydantic](https://img.shields.io/badge/typed%20with-pydantic-BA600F.svg?style=for-the-badge)](https://docs.pydantic.dev/)


## Motivation

Consistently Keeping the codebase to be maintainable and testable is always one of the struggle that many developers including myself has faced especailly when the project start growing and
becoming much more complex. Furthermore as more and more people get invovled, the extensibility and comphrehensibility of the codebase will become a huge liability.
Developer expected to upgrade their software with the latest and greatest features all the time and that can overwhelmed codebase and make it difficult to maintain If
things aren't built in a modular fashion.

Which is why I started looking at options to tackle this problem by exploring various standardization and guidelines (also known as architecure) of structuring
and bumps across various thoughts and ideas such as :
- clean architecture
- hexagonal architecture
- vertical slicing
- Onion/layer archiecture
- n-tiers architecture

This is one of the architectures that I am currently exploring and started working on the implementation parts to test out the theory as well as my overall understanding of the concepts.
Althought as a disclamers, I might not followed all the rules down to the granular details , the essence of theory is still there. Ultimately speaking, the most important goal of the
architecture is to establish a clear seperation of concerns in the codebase.


## Description

_Example Application Interface using FastAPI framework in Python 3_

This simple trello clone is a showcase of clean architecture implementation comprising of fastapi as the main http framework , sqlalchemy as the ORM and pydantic as the data model validator.
Clean architecture aims to improve the maintainability and extensibility of the software by maintaining one important goal which is clear seperation of concerns. To achieve such objective , the
codebase is divised into multiple layers that each handle different responsiblity.

## Heriachy of layers

Each layer varied in the level of abstraction and the pace of modification that it will have.
With the outer-most layer of the system dealing directly with framework dependent code such as the api controller, graphical interface ,database driver code and others commonly changed utilities.
The inner-most layer or the core represents the most stable part of the application. It contains important business logic that will fundementally drive the app overall behavoirs, Hence it won't be
regularly replaced.

Also Since Such rule is high-leveled by nature and often dervied directly from business requirements, It won't be expected to changed that regularly nor be affected by
other moving parts in the system. For instance , the change of auth logic or the way we access database will not cause any impact on the core business logic, for example the way we calculate discount
and taxes or certain crucial validation about user data, will be expected to stay intact.

<img src="https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg"/>

Some overview from the creator of the [Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## Installation process

_to be continued_

## Demoing

_to be continued_

## Acknowledgements

_to be continued_

## License

MIT License (see LICENSE).



