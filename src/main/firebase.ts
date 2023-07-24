import firebase, { initializeApp } from "firebase/app";
import { getFirestore, collection, getDocs, doc, getDoc, updateDoc, arrayUnion } from 'firebase/firestore';
import { getAnalytics } from "firebase/analytics";
import "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyCTe-FEPvszRgZ8eXO3CCIRHihbPD5br-k",
  authDomain: "exportlog-3e00e.firebaseapp.com",
  databaseURL: "https://exportlog-3e00e-default-rtdb.firebaseio.com",
  projectId: "exportlog-3e00e",
  storageBucket: "exportlog-3e00e.appspot.com",
  messagingSenderId: "31724899496",
  appId: "1:31724899496:web:f2772300132611f1f4c69d",
  measurementId: "G-79PF7EM8M5"
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);

// Initialize Firestore
const db = getFirestore(firebaseApp);

async function fetchData() {
  try {
    console.log('Attempting to fetch data');
    const docRef = doc(db, 'exportLog001', '1xlAXuv242ig2zqn2QOL');
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      console.log('Document found, data:', docSnap.data());
      // Assuming the data property of the document is an array
      return docSnap.data().exports || [];
    } else {
      console.log('No such document!');
      return [];
    }
  } catch (error) {
    console.error("Error getting document: ", error);
  }
};

async function appendData(
  date: string,
  time: string,
  stateQuantity: number,
  industryQuantity: number,
  VR: boolean,
  sunbelt: boolean
) {
  // Document reference
  const docRef = doc(db, 'exportLog001', '1xlAXuv242ig2zqn2QOL'); // Update the path as necessary

  // Data to append
  const newData = {
    date,
    time,
    stateQuantity,
    industryQuantity,
    VR,
    sunbelt,
  };

  try {
    // Append new data to 'exports' array in the document
    await updateDoc(docRef, {
      exports: arrayUnion(newData),
    });
    console.log("Data successfully appended!");
  } catch (error) {
    console.error("Error appending data: ", error);
  }
}

export { firebaseApp, db, fetchData, appendData };
