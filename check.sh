if ps -aux | grep -v grep | grep Manager.py
then
   echo 'Ja em Execucao!'  
else

    python3 /home/ubuntu/PythonServer/Manager.py & 
fi


