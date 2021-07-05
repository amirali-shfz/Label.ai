import api from '../apiService';
import {User} from '../user/userModel'

const classificationApi = {
  
  // Core api (blue) 2.1
  getClassificationProblem: async (): Promise<any> => {
    return await api.get('/images/prompt?count=1&user_id=1');
  },

  // Core api (blue) 2.2
  postClassificationSolution: async (solution:boolean, label: any, user: Partial<User>) => {
    const uid = user.userId || "1";
    await api.post('/submissions', {
      class_id: label.class_id,
      correct_label: solution,
      member_id: uid
    });
  },

  // Core api (blue) 3.1
  getAllLabels: async (): Promise<any> => {
    return await api.get('/labels/all');
  },

  // Core api (blue) 3.2
  getConfirmedImagesByLabel: async (labelId:string): Promise<any> => {
    return await api.get(`/images/confirmed?label_id="${labelId}"?`);
  },



};

export default classificationApi;