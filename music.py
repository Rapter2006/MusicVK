#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vkontakte
import urllib2
import subprocess
import os
import re


def printAllAudio(audio):
    subprocess.call("clear")
    for i in xrange(len(audio)):
        print str(i) + " " + audio[i]["artist"] + " - " + audio[i]["title"]


def downloadOnNumber(audio, number):
    nameFileNew = audio[number]["artist"] + " - " + audio[number]["title"]
    print "GET FILE: " + nameFileNew
    print "FILE NUMBER: " + str(number)
    subprocess.call(['wget', audio[number]["url"]])
    p = re.compile(r"[0-9a-zA-Z]+\.mp3$")
    nameFileOld = p.findall(audio[number]["url"])
    os.rename(nameFileOld[0], nameFileNew + ".mp3")


def dounloadAllFiles(audio):
    for i in xrange(len(audio)):
        downloadOnNumber(audio, i)


def downloadOnArtist(audio, artist):
    kol = 0
    for i in xrange(len(audio)):
        if audio[i]["artist"] in artist:
            downloadOnNumber(audio, i)
            kol += 1
    return kol


def downloadOnComposition(audio, composition):
    kol = 0
    for i in xrange(len(audio)):
        if audio[i]["title"] in composition:
            downloadOnNumber(audio, i)
            kol += 1
    return kol


def dowloadOnInterval(a, b):
    for i in xrange(a, b + 1):
        downloadOnNumber(audio, i)


def joinOther(x):
    answer = ''
    for i in xrange(2, len(x)):
        answer += x[i].decode("utf-8") + " "
    return answer


if __name__ == "__main__":

    subprocess.call("clear")
    tokenVK = 'http://oauth.vk.com/authorize?client_id=2996603&scope=audio&response_type=token'
    tokenVK = '' # получаем токен через свое приложение
    vk = vkontakte.API('2996603', 'czwzVJopa8vpupPcTe4c')
    vk = vkontakte.API(token=tokenVK)
#friends = vk.friends.get(fields = "first_name, last_name, bdate, contacts, photo_big", order = 'name')
    audio = vk.audio.get(uid='3757356')
    count = len(audio)
    print "Введите команду: "
    command = raw_input().split()
    if command[0] == "help":
        subprocess.call("clear")
        print "Доступные команды: "
        print "grub +"
        print "-all = скачать все песни из аудио"
        print "-s = скачать песню по её названию (пробел) название песни"
        print "-ar = скачать песню по название группы(имя артиста) (пробел) имя артиста(группы):"
        print "-print = распечатать все песни и их номер"
        print "-n = cкачать по номеру (пробел) номер песни"
        print "-i = скачать по интрервалу (пробел) первое число (пробел) второе число"
    elif command[0] == "grub":
        if command[1] == "-all":
            dounloadAllFiles(audio)
        elif command[1] == "-ar":
            kol = downloadOnArtist(audio, joinOther(command))
            if kol == 0:
                print "Нет совпадений в имени!"
        elif command[1] == "-s":
            kol = downloadOnComposition(audio, joinOther(command))
            if kol == 0:
                print "Нет совпадений в имени!"
        elif command[1] == "-print":
            printAllAudio(audio)
        elif command[1] == "-n":
            if command[2].isdigit() == False:
                print "Это не числовое значение!"
            elif 1 < int(command[2]) < count:
                downloadOnNumber(audio, int(command[2]))
            else:
                print "Песни с таким номером нет!"
        elif command[1] == "-i":
            if command[2].isdigit() == False or command[3].isdigit() == False:
                print "Это не числовое значение!"
            elif int(command[2]) > int(command[3]):
                print "Первое значение интервала должно быть меньше второго!"
            elif int(command[2]) < 1 or int(command[3]) < 1 or int(command[2]) > count or int(command[3]) > count:
                print "Введите значения от 1 до числа композиций"
            else:
                dowloadOnInterval(int(command[2]), int(command[3]))
    else:
        print command[0] + "- Не, не слышал :)"
