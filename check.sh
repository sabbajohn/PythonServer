if ps -aux | grep -v grep | grep Manager.py
then
   echo 'Ja em Execucao!'  
else

    sudo python3 /etc/PythonServer/Manager.py & 
fi

if ps -aux | grep -v grep | grep manage.py
then
   echo 'API ja em execução!'    
else
    sudo bash /etc/megaaapi2.0/runserver &
fi