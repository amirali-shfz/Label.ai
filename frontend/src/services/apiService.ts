import axios from 'axios';

const api = axios.create({
    baseURL: 'localhost:3001',
    timeout: 8000,
});

const noOpPromise = () => {
    return new Promise(resolve => {
        setTimeout(() => {
          resolve('resolved');
        }, 250);
      });
}
const testApi = {
    post: async (path:string, args: Object) => {
        switch (path){
            case '/user':
                return noOpPromise()
            case '/classification':
                return noOpPromise(); 
        }    
    },
    get: async (path:string) => {
        switch(path) {
            case '/user':
                return new Promise(resolve => {
                    setTimeout(() => {
                      resolve({
                          username: 'JohnDoe69',
                          userId: '6969',
                          trust: '0.1'
                      });
                    }, 250);
                  });
        }

    }

}

export default testApi;