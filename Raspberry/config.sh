#!/bin/bash
listop="update-bridge toggle-bridge toggle-wireless set-dhcpcd"
while [ $# -gt 0 ]; do
  arg=$1
  case $arg in
    update-bridge)
      cp /etc/cb/CBFi/bridge.conf /etc/network/interfaces.d/bridge
      break;;
    toggle-bridge)
      if [[ -n $2 ]]; then
        if [[ $2 == "on" ]]; then
          cp /etc/cb/CBFi/bridge.conf /etc/network/interfaces.d/bridge
          cp /etc/cb/CBFi/sysctl.conf.on /etc/sysctl.conf
          touch /etc/cb/CBFi/.BRIDGE_ENABLED
          echo "Bridge Enabled"
        else
          rm /etc/network/interfaces.d/bridge
          cp /etc/cb/CBFi/sysctl.conf.off /etc/sysctl.conf
          rm /etc/cb/CBFi/.BRIDGE_ENABLED
          echo "Bridge Disabled"
        fi
      else
        echo "Argument expected, see --arg-help toggle-bridge"
      fi
      break;;
    toggle-wireless)
      if [[ -n $2 ]]; then
        if [[ $2 == "ap" ]]; then
          if [[ ! -f /etc/cb/CBFi/.ENABLED  ]]; then
            cp /etc/cb/CBFi/hostapd.conf /etc/hostapd/hostapd.conf
            touch /etc/cb/CBFi/.ENABLED
            /lib/systemd/systemd-sysv-install enable hostapd
            /lib/systemd/systemd-sysv-install enable dhcpcd
            systemctl restart hostapd.service
            systemctl restart dhcpcd.service
            if [[ -f /etc/cb/CBFi/.CLIENTMODE ]]; then
              rm /etc/network/interfaces.d/wpa
              rm /etc/cb/CBFi/.CLIENTMODE
              systemctl stop wpa_supplicant
              systemctl disable wpa_supplicant > /dev/null 2> /dev/null
            fi
          fi
          echo "Access Point Enabled"
        else
          if [[ -f /etc/cb/CBFi/.BRIDGE_ENABLED ]]; then
            /etc/cb/config.sh toggle-bridge off
          fi
          if [[ -f /etc/hostapd/hostapd.conf ]]; then
            rm /etc/hostapd/hostapd.conf
            systemctl stop dhcpcd.service
            systemctl stop hostapd.service
            /lib/systemd/systemd-sysv-install disable hostapd
            /lib/systemd/systemd-sysv-install disable dhcpcd
          fi
          if [[ $2 == "client" ]]; then
            if [[ ! -f /etc/cb/CBFi/.CLIENTMODE ]]; then
              systemctl enable wpa_supplicant > /dev/null 2> /dev/null
              systemctl start wpa_supplicant
              cp /etc/cb/CBFi/wpa.conf /etc/network/interfaces.d/wpa
              touch /etc/cb/CBFi/.CLIENTMODE
              echo "Client Mode Enabled"
            fi
          else
            if [[ -f /etc/cb/CBFi/.CLIENTMODE ]]; then
              rm /etc/network/interfaces.d/wpa
              rm /etc/cb/CBFi/.CLIENTMODE
              systemctl stop wpa_supplicant
              systemctl disable wpa_supplicant > /dev/null 2> /dev/null
              echo "Client Mode Disabled"
            fi
          fi
          if [[ -f /etc/cb/CBFi/.ENABLED  ]]; then
            rm /etc/cb/CBFi/.ENABLED
            echo "Access Point Disabled"
          fi
        fi
      else
        echo "Argument expected, see --arg-help toggle-wireless"
      fi
      break;;
    set-dhcpcd)
      if [[ -n $2 ]]; then
        if [[ $2 == "default" ]]; then
          cp /etc/cb/CBFi/dhcpcd.conf.def /etc/dhcpcd.conf
          systemctl restart dhcpcd.service
          echo "dhcpcd set to default"
        elif [[ $2 == "static" ]]; then
          cp /etc/cb/CBFi/dhcpcd.conf.static /etc/dhcpcd.conf
          systemctl restart dhcpcd.service
          echo "dhcpcd set to static"
        elif [[ $2 == "fallback" ]]; then
          cp /etc/cb/CBFi/dhcpcd.conf.fallback /etc/dhcpcd.conf
          systemctl restart dhcpcd.service
          echo "dhcpcd set to fallback"
        else
          echo "Unknown argument, see --arg-help set-dhcpcd"
        fi
      else
        echo "Argument expected, see --arg-help set-dhcpcd"
      fi
      break;;
    --arg-help)
      if [[ -n $2 ]]; then
        case $2 in
          toggle-bridge)
            echo "on off"
            break;;
          toggle-wireless)
            echo "ap client off"
            break;;
          set-dhcpcd)
            echo "default static fallback"
            break;;
        esac
      else
        echo $listop
      fi
      break;;
    *)
     echo "Unknown argument {${arg}}, see --arg-help"
     break;;
  esac
  shift
done
