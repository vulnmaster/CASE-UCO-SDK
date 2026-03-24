.PHONY: all generate build test clean init

all: init generate build test

init:
	git submodule update --init --recursive
	pip install -e generator/

generate:
	python -m case_uco_generator generate --lang all

build: build-python build-csharp build-java build-rust

build-python:
	cd python && pip install -e .

build-csharp:
	cd csharp && dotnet build

build-java:
	cd java && mvn package -q

build-rust:
	cd rust && cargo build

test: test-generator test-python test-csharp test-java test-rust

test-generator:
	PYTHONPATH=generator/src python -m pytest generator/tests/ -v

test-python:
	cd python && python -m pytest tests/ -v

test-csharp:
	cd csharp && dotnet test

test-java:
	cd java && mvn test -q

test-rust:
	cd rust && cargo test

clean:
	rm -rf python/case_uco/uco/*.py python/case_uco/case/*.py
	rm -rf csharp/CaseUco/Uco/*.cs csharp/CaseUco/Case/*.cs
	find java/src/main/java/org/caseontology -name "*.java" -not -name "CaseGraph.java" -delete
	rm -rf rust/src/uco/*.rs rust/src/case/*.rs
