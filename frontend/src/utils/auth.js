export const getAccessToken = () => {
  return localStorage.getItem("access_token");
};

export const isAuthenticated = () => {
  return Boolean(getAccessToken());
};

export const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};