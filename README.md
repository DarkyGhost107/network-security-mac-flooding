# MAC Flooding - Laboratorio de Seguridad de Redes

**Ambiente:** GNS3 (Controlado) | **Herramienta:** Python 3 + Scapy | **Capa OSI:** Capa 2

## Aviso Legal

Uso **exclusivamente educativo** en laboratorio controlado (GNS3). El uso no autorizado es **ilegal**.

## 1. Objetivo del Laboratorio

Demostrar el ataque MAC Flooding (CAM Table Overflow): el atacante inunda la tabla CAM del switch con miles de entradas MAC falsas hasta agotarla. Una vez llena, el switch no puede aprender nuevas MACs y comienza a comportarse como un HUB, enviando los frames a todos los puertos, lo que permite capturar trafico ajeno.

## 2. Objetivo del Script

`mac_flooding.py` envia masivamente frames Ethernet con MACs fuente y destino aleatorias. Cada frame unico fuerza al switch a crear una nueva entrada en su tabla CAM hasta desbordarla.

## 3. Parametros del Script

| Parametro | Flag | Tipo | Default | Descripcion |
|-----------|------|------|---------|-------------|
| Interfaz | `-i` | str | eth0 | Interfaz de red |
| Cantidad | `-c` | int | 5000 | Numero de frames a enviar |
| Delay | `-d` | float | 0.0 | Pausa entre frames (0 = max velocidad) |

### Ejemplo de uso

```bash
sudo python3 mac_flooding.py
sudo python3 mac_flooding.py -c 50000
sudo python3 mac_flooding.py -c 10000 -d 0.001
```
![Texto alternativo](https://github.com/DarkyGhost107/network-security-mac-flooding/blob/main/screenshots/eje%20mac%20flooding%20script.png)

## 4. Requisitos

```bash
Python 3.8+
pip install scapy
root (sudo)
```

## 5. Funcionamiento del Script

```
NORMAL (tabla CAM sana):
  Frame de A->B: switch envia SOLO al puerto de B

DESPUES DEL ATAQUE (tabla CAM llena):
  Frame de A->B: switch envia a TODOS los puertos
                      |            |            |
                  Puerto 1      Puerto 2   Puerto 3 (atacante captura)
```

Para cada frame:
1. Genera MAC fuente aleatoria (src_mac)
2. Genera MAC destino aleatoria (dst_mac)
3. Construye frame Ethernet con IPs/UDP aleatorios
4. Envia via sendp() por la interfaz
5. Switch registra src_mac -> puerto atacante en tabla CAM
6. Tabla CAM se llena (tipicamente 4K-16K entradas)
7. Switch activa modo FAIL-OPEN (flooding a todos)

## 6. Topologia de Red (GNS3)

![Texto alternativo](https://github.com/DarkyGhost107/network-security-mac-flooding/blob/main/screenshots/topologia%20Mac%20Flooding.png)

### Direccionamiento

| Dispositivo | IP | Rol |
|-------------|-----|-----|
| Host A | 192.168.1.10/24 | Victima - trafico expuesto |
| Host B | 192.168.1.20/24 | Victima - trafico expuesto |
| Switch | — | Objetivo del MAC Flood |
| Atacante | 192.168.1.50/24 | Lanza el ataque |

## 7. Capturas de Pantalla

Coloca tus capturas en `screenshots/`:
- `screenshots/cam_table_before.png` - Tabla CAM normal
  ![Texto alternativo](https://github.com/DarkyGhost107/network-security-mac-flooding/blob/main/screenshots/Mac%20address%20table.png)
- `screenshots/mac_flood_running.png` - tabla dinamica
- ![Texto alternativo](https://github.com/DarkyGhost107/network-security-mac-flooding/blob/main/screenshots/mac%20address%20dynamic%20con%20el%20script.png)
- `screenshots/cam_table_full.png` - Tabla CAM desbordada
- ![Texto alternativo](https://github.com/DarkyGhost107/network-security-mac-flooding/blob/main/screenshots/mac%20address%20table%20con%20script.png)

## 8. Contramedidas

| Contramedida | Comando Cisco IOS | Descripcion |
|---|---|---|
| Port Security | `switchport port-security` | Limita MACs por puerto |
| Max MACs | `switchport port-security maximum 2` | Solo N MACs por puerto |
| Accion violacion | `switchport port-security violation shutdown` | Apaga el puerto si se supera el limite |

```cisco
interface range GigabitEthernet0/1 - 24
 switchport mode access
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation restrict
 switchport port-security aging time 5
show port-security interface GigabitEthernet0/1
```
![Texto alternativo](https://github.com/DarkyGhost107/network-security-mac-flooding/blob/main/screenshots/contramedida%20mac%20flooding.png)

## 9. Referencias

- [MITRE ATT&CK T1557 - Adversary-in-the-Middle](https://attack.mitre.org/techniques/T1557/)
- [Cisco Port Security Best Practices](https://www.cisco.com/c/en/us/support/docs/lan-switching/port-security/11841-port-security.html)

## 10.Enlaces
Video:https://youtu.be/SfjPA316Xn8
---
*Laboratorio de Seguridad de Redes | GNS3 | Uso educativo exclusivo*
