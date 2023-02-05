import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [currentMessage, setCurrentMessage] = useState(0);

  // useEffect(() => {
  //   fetch('/hello').then(res => res.json()).then(data => {
  //     console.log(data);
  //     setCurrentMessage(data.message);
  //   });
  // }, []);

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


class InventoryItem extends React.Component {
  constructor(props) {
    super(props);
    console.log("Inventory Item just got constructed!")
    console.log(props)
  }

  render() {
    return (
      <div className="domain-card">
        <div>{this.props.product.item_name}</div>
        <div>Item: {this.props.product.upc}</div>
        <div>Qty Remaining: {this.props.product.qty_percentage_remaining}</div>
      </div>
    )
  }
}

// class DomainCategory extends React.Component {
//   constructor(props) {
//     super(props);
//     console.log("Creating category for " + this.props.category);
//     console.log(props)
//   }

//   render() {
//     const domains = this.props.domains.map((domain) => {
//       return <Domain key={domain.name} mydomain={domain} />
//     })
//     return (
//       <div className="domain-category">
//         <div>{this.props.category}</div>
//         <div>{domains}</div>
//       </div>
//     )
//   }
// }

class InventoryCategoryView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inventory: []
    }

    // Get the inventory list for a user!
    fetch('/inventory').then(res => res.json()).then(data => {
      console.log("Collecting Inventory of Products!")
      console.log(data);
      this.setState({
        inventory: data.inventory
      });
    });

  }
  render() {
    const inventory_list = this.state.inventory.map((product) => {
      return (
          <Product key={product.upc} product={product} />
      )
    });
    return (
      <div className="verticalbuffer">
        {inventory_list}
      </div>
    )
  }
}


class Product extends React.Component {
  constructor(props) {
    super(props);
    console.log("I just got constructed!")
    console.log(props)
  }

  render() {
    return (
      <div className="domain-card">
        <img src={this.props.product.image_url}/>
        <div>{this.props.product.title}</div>
        <div>{this.props.product.upc}</div>
        <div>{this.props.product.brand}</div>
        <div>{this.props.product.model}</div>
        <div>{this.props.product.category}</div>
      </div>
    )
  }
}

class ProductList extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      inventory: []
    }

    // Get the product list!
    console.log("Sending an API call to get the inventory.")
    fetch('/product').then(res => res.json()).then(data => {
      console.log("Collecting Inventory of Products!")
      console.log(data);
      this.setState({
        inventory: data.inventory
      });
    });

  }
  render() {
    const inventory_list = this.state.inventory.map((product) => {
      return (
          <Product key={product.upc} product={product} />
      )
    });
    return (
      <div className="verticalbuffer">
        {inventory_list}
      </div>
    )
  }
}

class InventoryList extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      inventory: []
    }

    // Get the inventory list!
    console.log("Sending an API call to get the inventory.")
    fetch('/inventory?populate_details=true').then(res => console.log(res));
    fetch('/inventory').then(res => res.json()).then(data => {
      console.log("Collecting Inventory!")
      console.log(data);
      this.setState({
        inventory: data.inventory
      });
    });

  }

  populate_details(inventory) {
    // TODO
    console.log(inventory);
  }

  render() {
    const inventory_list = this.state.inventory.map((product) => {
      return (
          <InventoryItem key={product.item_name} product={product} />
      )
    });
    return (
      <div className="verticalbuffer">
        <div id="inventory_list">
          {inventory_list}
        </div>
      </div>
    )
  }
}

class MyApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {

    };
  }

  render () {
    return (
      <div id="background">
        <div id="greeting-card">
          <div id="pantry-text">
            <h1>Pantry</h1>
          </div>
          <div id="greeting">
            <h3>Hello, Rodney!</h3>
          </div>
        </div>

        <InventoryList/>
        <ProductList/>
      </div>
    );

  }

}
export default MyApp;
// export default App;