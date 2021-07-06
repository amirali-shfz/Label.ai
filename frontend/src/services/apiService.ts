import axios from 'axios';
import _ from 'lodash';

const api = axios.create({
    baseURL: 'localhost:8000',
    timeout: 8000,
});

const returnPromise = (retVal: any) => {
    return new Promise(resolve => {
        setTimeout(() => {
          resolve(retVal);
        }, 250);
      });
}
const randomString = ():string => {return Math.random().toString().substring(16)}

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
        const trimmed = path.split('?')[0] 
        console.log("trimmed request path: ", trimmed)
        switch(trimmed) {
            case '/user':
                return returnPromise({})
            case '/images/prompt':
                return returnPromise({
                    prompt: [
                        {
                            url: _.sample(
                            ['https://c7.staticflickr.com/1/35/70594660_499be9e349_o.jpg',
                            'https://c5.staticflickr.com/9/8185/8121565107_718c80b0ef_o.jpg',
                            'https://farm3.staticflickr.com/8055/8110769165_9ef5f4da70_o.jpg',
                            'https://thumbs.dreamstime.com/b/dubai-uae-february-vertical-panorama-burj-khalifa-as-viewed-water-canal-143096793.jpg']),
                            image_id: randomString(),
                            labels: [{label_id: randomString(), label_name: randomString(), class_id: randomString()}],}
                        ]
                });
            case '/labels/all':
                return returnPromise({
                    labels: [{label_id: '1', label_name: 'label 1'},{label_id: '2', label_name: 'label 2'},{label_id: '3', label_name: 'label 3'} ]
                });
            case '/images/confirmed':
            case '/images/mislabelled':
            case '/images/underclassified':
                return returnPromise({
                    images: [{url: 'https://c7.staticflickr.com/1/35/70594660_499be9e349_o.jpg'},
                    {url:'https://c5.staticflickr.com/9/8185/8121565107_718c80b0ef_o.jpg'},
                    {url:'https://farm3.staticflickr.com/8055/8110769165_9ef5f4da70_o.jpg'},
                    {url:'https://thumbs.dreamstime.com/b/dubai-uae-february-vertical-panorama-burj-khalifa-as-viewed-water-canal-143096793.jpg'}]
                })
        }

    }

}

// no op
testApi!;
api!;

export default testApi;