import { count } from "console";
import api from "../apiService";
import { User } from "../user/userModel";

const classificationApi = {
  // Core api (blue) 2.1
  getClassificationProblem: async (params: {
    user_id: string,
    label_id: string,
    count: number,
  }): Promise<any> => {
    console.log('pms',params)
    const res = await api.get("/images/prompt", {
      params,
    });
    return res.data;
  },

  // Core api (blue) 2.2
  postClassificationSolution: async (
    is_true_label: boolean | null,
    label: any,
    user?: User
  ) => {
    const uid = user?.userId || "1";
    const correct_label =
      is_true_label == null ? "idk" : is_true_label ? "t" : "f";

    await api.post("/submissions/insert", {
      class_id: label.class_id,
      correct_label,
      member_id: uid,
    });
    return;
  },

  // Core api (blue) 3.1
  getAllLabels: async (): Promise<any> => {
    const res = await api.get("/labels/all");
    return res.data;
  },

  getImages: async(endpoint:string, count:number, label_id:string|null = null): Promise<Array<Object>> => {

    var params : any = {'count' : count}
    if (label_id && label_id.length) {
      params.label_id = label_id
    }
    console.log(params)
    console.log(label_id)
    const res = await api.get(`/images/${endpoint}/`, {params: params});
    return res.data;
  },

  // Core api (blue) 3.2
  getConfirmedImagesByLabel: async (label_id: string): Promise<any> => {
    const res = await api.get(`/images/confirmed/`, {
      params: {
        label_id,
      },
    });
    return res.data;
  },

  // 5.1
  getMislabelledImages: async (count: number): Promise<any> => {
    const res = await api.get(`/images/mislabelled/`, {
      params: {
        count,
      },
    });
    return res.data;
  },

  // 5.2
  getUnderclassifiedImages: async (count: number): Promise<any> => {
    const res = await api.get(`/images/underclassified/`, {
      params: {
        count,
      },
    });
    return res.data;
  },
};

export default classificationApi;
