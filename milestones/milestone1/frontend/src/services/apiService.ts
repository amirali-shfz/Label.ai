import axios from 'axios';
import _ from 'lodash';
import { textChangeRangeIsUnchanged } from 'typescript';

const api = axios.create({
    baseURL: 'localhost:3001',
    timeout: 8000,
});

const returnPromise = (retVal: any) => {
    return new Promise(resolve => {
        setTimeout(() => {
          resolve(retVal);
        }, 250);
      });
}
const randomString = ():string => {return Math.random.toString().substring(16)}

const testApi = {
    post: async (path:string, args: Object) => {
        switch (path){
            case '/user':
                return returnPromise('200')
            case '/classification':
                return returnPromise('200')
        }    
    },
    get: async (path:string) => {
        switch(path) {
            case '/user':
                return returnPromise({})
            case '/image/random':
                return returnPromise({
                    url: _.sample(
                        ['https://c7.staticflickr.com/1/35/70594660_499be9e349_o.jpg',
                         'https://c5.staticflickr.com/9/8185/8121565107_718c80b0ef_o.jpg',
                         'https://farm3.staticflickr.com/8055/8110769165_9ef5f4da70_o.jpg']),
                    iid: randomString(),
                    label: [{lid: randomString(), name: randomString()}],
                })
        }

    }

}

export default testApi;