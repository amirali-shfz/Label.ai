import axios from 'axios';
import _ from 'lodash';

const api = axios.create({
    baseURL: 'http://localhost:8000',
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
            case '/members':
                return returnPromise('200')
            case '/classification':
                return returnPromise('200')
        }    
    },
    get: async (path:string) => {
        const trimmed = path.split('?')[0];
        console.log("trimmed request path: ", trimmed)
        switch(trimmed) {
            case '/members':
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
                return returnPromise({
                    images: [{url: 'https://c7.staticflickr.com/1/35/70594660_499be9e349_o.jpg'},
                    {url:'https://c5.staticflickr.com/9/8185/8121565107_718c80b0ef_o.jpg'},
                    {url:'https://farm3.staticflickr.com/8055/8110769165_9ef5f4da70_o.jpg'},
                    {url:'https://thumbs.dreamstime.com/b/dubai-uae-february-vertical-panorama-burj-khalifa-as-viewed-water-canal-143096793.jpg'}]
                })
            case '/images/mislabelled':
            case '/images/underclassified':
                return returnPromise({
                    images: [
                        {
                            "url": "https://c3.staticflickr.com/7/6028/5956647590_bee0e724af_o.jpg",
                            "image_id": "4ee715bebe1d3bca",
                            "labels": [
                                {
                                    "label_id": "04rky",
                                    "label_name": "Mammal",
                                    "class_id": 4142,
                                    "confidence": "0.44"
                                }
                            ]
                        },
                        {
                            "url": "https://c2.staticflickr.com/5/4031/4505653924_4fe8a59bf9_o.jpg",
                            "image_id": "13385cd3493d5fe9",
                            "labels": [
                                {
                                    "label_id": "0dzct",
                                    "label_name": "Human face",
                                    "class_id": 1012,
                                    "confidence": "0.69"
                                }
                            ]
                        },
                        {
                            "url": "https://farm6.staticflickr.com/13/16383286_2e1b11206a_o.jpg",
                            "image_id": "3b8c56a26abf57c5",
                            "labels": [
                                {
                                    "label_id": "01g317",
                                    "label_name": "Person",
                                    "class_id": 3144,
                                    confidence: "0.33"
                                }
                            ]
                        },
                        {
                            "url": "https://c7.staticflickr.com/3/2682/4232861778_0f91c7273a_o.jpg",
                            "image_id": "3767728c5b4e2b4e",
                            "labels": [
                                {
                                    "label_id": "05r655",
                                    "label_name": "Girl",
                                    "class_id": 2918,
                                    "confidence": "0.55"
                                }
                            ]
                        }
                    ]
                })
        }

    }

}

// no op
testApi!;
api!;

export default api;