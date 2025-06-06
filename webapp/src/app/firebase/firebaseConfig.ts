import { initializeApp } from "firebase/app";
import { getAnalytics, isSupported as analyticsIsSupported } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { environment } from '../../environments/environment';

const firebaseConfig = {
  apiKey: environment.firebase.apiKey,
  authDomain: environment.firebase.authDomain,
  projectId: environment.firebase.projectId,
  storageBucket: environment.firebase.storageBucket,
  messagingSenderId: environment.firebase.messagingSenderId,
  appId: environment.firebase.appId,
  measurementId: environment.firebase.measurementId
};

const app = initializeApp(firebaseConfig);

// Only initialize analytics if supported (i.e., in the browser)
if (typeof window !== 'undefined') {
  analyticsIsSupported().then((supported) => {
    if (supported) {
      getAnalytics(app);
    }
  });
}

export const auth = getAuth(app);
export default app;