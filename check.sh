if ps -aux | grep -v grep | grep Manager.py
then
   echo 'Ja em Execucao!'  
else

    sudo python3 /etc/PythonServer/Manager.py & 
fi

