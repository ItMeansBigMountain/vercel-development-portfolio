import React from 'react';
import { createRoot } from 'react-dom/client'; 
import './index.css';
import App from './App';


const root = document.getElementById("root");
const reactRoot = createRoot(root);  

reactRoot.render(<App/>);  





// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import './index.css';
// import App from './App';

// ReactDOM.render(<App/>, document.getElementById("root")); 