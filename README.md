# Kitchen App
A Kivy mobile application packaged for android using Buildozer.

## Overview
Kitchen App is a mobile application built using Python and Kivy. 
It tracks inventory and expiration dates for food items and stores recipes 
that can be added to a shopping list with the click of a button.

This app is fully CI/CD automated with the options to both containerize the project and 
upload it to Github as and image and the ability to package it as a .apk automatically and upload it to Github.

## Building the APK
git tag apk-0.1
git push origin apk-0.1

using these git tag commands will trigger the automated packaging in buildozer and upload it to Github releases.

## Containerizing the app with Docker
Pushing to main will trigger the creation of a Docker image and run tests inside the container, 
then it is pushed to the Github Container Registry
