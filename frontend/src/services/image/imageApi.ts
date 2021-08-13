import api from '../apiService';
import {User} from '../user/userModel'

const classificationApi = {
  
  // Core api (blue) 2.1
  getClassificationProblem: async (): Promise<any> => {
    const res = await api.get('/images/prompt', {
      params:
      {
        'count':1,
        'user_id':1
      }
    });
    return res.data;
  },

  // Core api (blue) 2.2
  postClassificationSolution: async (is_true_label:boolean|null, label: any, user: Partial<User>) => {
    const uid = user.userId || "1";
    const correct_label = is_true_label == null ? 'idk' : is_true_label ? 't' : 'f';

    await api.post('/submissions/insert', {
      class_id: label.class_id,
      correct_label,
      member_id: uid
    });
    return;
  },

  // Core api (blue) 3.1
  getAllLabels: async (): Promise<any> => {
    const res = await api.get('/labels/all');
    return res.data;
  },

  // Core api (blue) 3.2
  getConfirmedImagesByLabel: async (label_id:string): Promise<any> => {
    const res = await api.get(`/images/confirmed/`,
    {
      params: {
        label_id
      }
    });
    return res.data;
  },

  // 5.1
  getMislabelledImages: async (count:number): Promise<any> => {
    const res = await api.get(`/images/mislabelled/`,
    {
      params: {
        count
      }
    });
    return res.data;
  },

  // 5.2
  getUnderclassifiedImages: async (count:number): Promise<any> => {
    const res = await api.get(`/images/underclassified/`,{
    params: {
      count
    }});
    return res.data;
  },
};

export default classificationApi;