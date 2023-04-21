import logo from './logo.svg';
import './App.css';

function App() {
   // Returns a list of items by kind via callback
   const fetchList = (kind,callback) => {
      fetch(`data/${kind}`)
      .then(response => {
         if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
         }
         return response.json()
      })
      .then(data => {
         if (callback) {
            callback(data)
         }
      })
      .catch(error => {
         console.log(error);
      })
   }
   // Returns a specific item by kind and name via callback
   const fetchItem = (kind,name,callback) => {
      fetch(`data/${kind}/${name}`)
      .then(response => {
         if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
         }
         return response.json()
      })
      .then(data => {
         if (callback) {
            callback(data)
         }
      })
      .catch(error => {
         console.log(error);
      })
   }
   // Examples that you can remove
   fetchList('experiments',(data) => console.log(data));
   fetchItem('experiments','E37481',(data) => console.log(data));

   // Your application here
   return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
   );
}

export default App;
