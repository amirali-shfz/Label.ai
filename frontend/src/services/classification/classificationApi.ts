import api from '../apiService';
import {User} from '../user/userModel'
const classificationApi = {
  getClassificationProblem: async () => {
    return await api.get('/classification');
  },

  postClassificationSolution: async (cId: string, label:string, solution:boolean, user: User) => {
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