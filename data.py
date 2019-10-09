class Data(object):
    
    def __init__(self):
        self.primeiro = 0
        self.tamanho = 0
        self.data = []
        primeiro =self.primeiro
        tamanho =self.tamanho
        data = self.data

    def get_data(self):
        if tamanho > 0:
            primeiro = primeiro+1
            tamanho = tamanho-1
            return data['self.primeiro-1']
        else:
            return tamanho
    
    def set_data(self,response):
        data.append(response)
        tamanho =tamanho+1
        
