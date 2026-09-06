const CONFIG = require("../api_config/config.json")




class Server_object {
  constructor(lastItem, all_stocks) {
    this.lastItem = lastItem;
    this.all_stocks = all_stocks
  }


  // HTTP REQUEST
  static fetch_stocks = async () => {
    let response = await fetch(
      // `${CONFIG.base_url}/api/build_internal`
      'https://dumbstockapi.com/stock?exchanges=NASDAQ'
    );
    let json = await response.json();
    return json;
  }

  

  
  

  // CHUNK API REQUEST DATA 
  static chunking = (qty, arr_object, lastItemIndex) => {
    let newArr;

    // check if list complete
    if (lastItemIndex === arr_object.length - 1) return ["done"];

    // INIT all_stocks state
    if (!this.lastItem) {
      // console.log('>>>>>> onEvent()  ', lastItemIndex)
      newArr = [...arr_object].slice(0, qty);
      this.lastItem = [...newArr].pop();
    }

    // UPDATE all_stocks state
    else {
      // console.log('<<<<<< updating  ', lastItemIndex)
      newArr = [...arr_object].slice(lastItemIndex, qty + lastItemIndex);
      this.lastItem = [...arr_object].pop();
    }

    return newArr

  }


  
}








const s = new Server_object("", Server_object.fetch_stocks().then(r => r) )


export const fetch_rendered_data = (qty, index) => {
  const arr = Server_object.fetch_stocks()
    .then(promise_object => Server_object.chunking(qty, promise_object, index))
  return arr;
}


