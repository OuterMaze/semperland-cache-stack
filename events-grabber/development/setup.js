// These lines must be run inside a Ganache console where the Metaverse
// contract, and its friends, are deployed.

// 1.1. Have this utility function.
function toEthBN(v) { return web3.utils.toBN(web3.utils.toWei("10")); }

// 1.2. Also, have this metaverse address.
let metaverse = await Metaverse.deployed()

// 1.3. Also, have the brand registry.
let brandRegistry = await BrandRegistry.deployed()

// Sample brand events.

// 2.1. accounts[0] mints "Coca Cola" brand for themselves.
await brandRegistry.registerBrand("0x", "Coca Cola", "The Coca Cola company", "https://static.cocacola.com/image.png", "https://static.cocacola.com/icon16.png", "https://static.cocacola.com/icon32.png", "https://static.cocacola.com/icon64.png")

// 2.2. account[1] mints "Pepsi" brand for themselves (pays 10eth).
await brandRegistry.registerBrand("0x", "PepsiCo", "PepsiCo", "https://static.pepsico.com/image.png", "https://static.pepsico.com/icon16.png", "https://static.pepsico.com/icon32.png", "https://static.pepsico.com/icon64.png", {from: accounts[1], value: toEthBN("10")})

// 2.3. accounts[2] mints "Samsung" brand for themselves (pays 10eth).
await brandRegistry.registerBrand("0x", "Samsung", "Samsung Electronics", "https://static.samsung.com/image.png", "https://static.samsung.com/icon16.png", "https://static.samsung.com/icon32.png", "https://static.samsung.com/icon64.png", {from: accounts[2], value: toEthBN("10")})

// 2.4. accounts[3] mints "Apple" brand for themselves (pays 10eth).
await brandRegistry.registerBrand("0x", "Apple", "Apple", "https://static.apple.com/image.png", "https://static.apple.com/favicon16.png", "https://static.apple.com/favicon32.png", "https://static.apple.com/favicon64.png", {from: accounts[3], value: toEthBN("10")})

// 2.5. accounts[4] mints "Alphabet" brand for themselves (pays 10eth).
await brandRegistry.registerBrand("0x", "Alphabet", "The Alphabet company", "https://static.alphabet.com/image.png", "https://static.alphabet.com/fav16.png", "https://static.alphabet.com/fav32.png", "https://static.alphabet.com/fav64.png", {from: accounts[4], value: toEthBN("10")})

// 2.6. Now, get the brands IN ORDER.
const brandRegisteredEvents = await brandRegistry.getPastEvents("BrandRegistered", {fromBlock: 0, toBlock: "latest"})
const brandIds = brandRegisteredEvents.map((bre) => bre.args.brandId)

// 3.1. Set the brand registration cost. First to 15, then fix to 20.
await brandRegistry.setBrandRegistrationCost(toEthBN("15"))
await brandRegistry.setBrandRegistrationCost(toEthBN("20"))

// 3.2. Set the brand registration earnings receiver.
await brandRegistry.setBrandRegistrationEarningsReceiver(accounts[1])
await brandRegistry.setBrandRegistrationEarningsReceiver(accounts[0])

// 3.3. Set the social commitment for Alphabet and Samsung. Then, regret Google.
await brandRegistry.updateBrandSocialCommitment(brandIds[2], true)
await brandRegistry.updateBrandSocialCommitment(brandIds[2], false)
await brandRegistry.updateBrandSocialCommitment(brandIds[4], true)

// 3.4. Update the image of a brand and also the challenge url of Samsung.
await brandRegistry.updateBrandImage("0x", brandIds[1], "https://static.pepsico.com/new-image.png", {from: accounts[1]})
await brandRegistry.updateBrandImage("0x", brandIds[2], "https://www.samsung.com/challenge.json", {from: accounts[2]})

// 3.5. Update the icons of brands.
await brandRegistry.updateBrandIcon16x16Url("0x", brandIds[3], "https://static.apple.com/favicon16.png", {from: accounts[3]})
await brandRegistry.updateBrandIcon32x32Url("0x", brandIds[3], "https://static.apple.com/favicon32.png", {from: accounts[3]})
await brandRegistry.updateBrandIcon64x64Url("0x", brandIds[3], "https://static.apple.com/favicon64.png", {from: accounts[3]})

// 3.4. Brand permissions management.
const brandAesthetics = web3.utils.keccak256("BrandRegistry::Brand::Edit")
await brandRegistry.brandSetPermission("0x", brandIds[4], brandAesthetics, accounts[7], true, {from: accounts[4]})
await brandRegistry.brandSetPermission("0x", brandIds[4], brandAesthetics, accounts[7], false, {from: accounts[4]})
await brandRegistry.brandSetPermission("0x", brandIds[4], brandAesthetics, accounts[8], true, {from: accounts[4]})
await brandRegistry.brandSetPermission("0x", brandIds[4], brandAesthetics, accounts[8], false, {from: accounts[4]})
await brandRegistry.brandSetPermission("0x", brandIds[4], brandAesthetics, accounts[8], true, {from: accounts[4]})

// 3.5. Some metaverse-level permissions assignment.
const mintBeat = web3.utils.keccak256("Plugins::Currency::BEAT::Mint")
const currencySettingsManage = web3.utils.keccak256("Plugins::Currency::Settings::Manage")
await metaverse.setPermission(mintBeat, accounts[10], true)
await metaverse.setPermission(currencySettingsManage, accounts[11], true)
await metaverse.setPermission(mintBeat, accounts[10], false)

let sponsorRegistry = await SponsorRegistry.deployed()

await sponsorRegistry.setSponsor(accounts[11], true)
await sponsorRegistry.setSponsor(accounts[11], false)
await sponsorRegistry.setSponsor(accounts[12], true)
await sponsorRegistry.setSponsor(accounts[12], false)
await sponsorRegistry.setSponsor(accounts[12], true)
await sponsorRegistry.setSponsor(accounts[13], true)

await sponsorRegistry.sponsor(brandIds[4], true, {from: accounts[12]})
await sponsorRegistry.sponsor(brandIds[3], true, {from: accounts[13]})
await sponsorRegistry.sponsor(brandIds[4], false, {from: accounts[12]})

////////////////////////////// TODAS, HASTA ACÁ, YA LAS CORRÍ.

