import apiClient from './axios';

export const userAPI = {
  // 注册用户
  register(userData) {
    return apiClient.post('/register/', userData);
  },

  // 用户登录
  login(userData) {
    return apiClient.post('/login/', userData);
  },

  // 删除账户
  deleteAccount(password, token) {
    return apiClient.delete('/delete-account/', {
      headers: { 'Authorization': `Bearer ${token}` },
      data: { password }
    });
  },

  // 上传头像
  uploadAvatar(formData, token) {
    return apiClient.post('/upload-avatar/', formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 更新简介
  updateBio(bio, token) {
    return apiClient.patch('/update-bio/', { bio }, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  },

};