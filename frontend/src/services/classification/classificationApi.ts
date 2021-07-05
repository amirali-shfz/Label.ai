import api from '../apiService';
import {User} from '../user/userModel'

const classificationApi = {
  getClassificationProblem: async (): Promise<any> => {
    return await api.get('/image/random');
  },

  postClassificationSolution: async (cId: string, label:string, solution:boolean, user: Partial<User>) => {
    const uid = user.userId;
    await api.post('/classification', {
      cId,
      label,
      solution,
      uid
    });
  },

};

export default classificationApi;