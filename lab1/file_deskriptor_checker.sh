#!/bin/bash
echo "Программа отслеживания изменений индексного дескриптора файлов.
      Чтобы проверить был ли изменён дескриптор файла с определённого момента времени  необходимо ввести его имя и интересующую дату.
	    Чтобы выйти в любой момент из программы можно ввести команду /exit.
	    Creator: Кармишкин В.Д. 717-1 группа. ФБ"

readonly exit_cmd="/exit"
readonly exit_status=120

last_input=""
datetime=""
err_flag=0

function check_exit_input_cmd() {
	if [ "$last_input" == "$exit_cmd" ]; then exit 0; else return 1; fi;
}

function echo-err {
	echo "$1" > /dev/stderr;
}
function set_err_flag {
  err_flag=$1
}
function read_date {
	while : ; do
		echo -n "Введите дату (формат даты (YYYY-MM-DD): "
		read datetime
		# Условие проверяет по регулярке + проверяет существует ли дата за счёт корректного ответа комманды date.
    if [[ $datetime =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] && date -d "$datetime" >/dev/null; then
      break;
    else
      echo-err "Введёные данные $datetime не соотвествуют формату YYYY-MM-DD или не существует";
    fi
	done
}

function continueOrExit() {
  while true ; do
    read -rp "Хотите начать заново? (y/n): "
    case "$REPLY" in
      y ) return ;;
      n )
        if [[ $err_flag -eq 1 ]]; then
          exit $exit_status
        else
          exit 0
        fi ;;
      * ) echo -n "Введите 'y' или 'n'" ;;
    esac
  done
}

while : ; do
  set_err_flag 0
  echo "Текущая директория: $PWD";

  while true ;do

      echo  -n 'Введите имя файла: '
      read filename
      NAME=$PWD/$filename

      last_input="$filename"
      check_exit_input_cmd

      if  [ ! -f $NAME ]; then
        echo-err "Ошибка! Файла с именем $filename не существует в данной директории!"
      else
        last_input="$filename"
        break;
      fi
  done

      read_date
      time_entered=$(date -d "$datetime" +%s) # В секундах для сравнения
      echo "Вы ввели дату $(date -d "$datetime")"
      last_descriptor_updated=$(date -d "$(stat -c %z $filename)") # Для пользователя
      last_descriptor_updated_sec=$(date -d "$(stat -c %z $filename)" +%s) # В секундах для сравнения

      if  [[ $time_entered -le $last_descriptor_updated_sec  ]]; then
          echo "Дескриптор файла  $filename изменялся после введёной даты. Время изменения: $last_descriptor_updated"
          exit $exit_status;
      else
          echo-err  "Дескриптор не изменялся после введённой даты (Последнее изменение было $last_descriptor_updated)";
          set_err_flag 1
      fi

  continueOrExit
done
