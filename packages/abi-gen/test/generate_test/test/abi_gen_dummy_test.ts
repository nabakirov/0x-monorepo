import { BlockchainLifecycle, devConstants, web3Factory} from '@0x/dev-utils';
import { Web3ProviderEngine } from '@0x/subproviders';
import { RevertReason } from '@0x/types';
import { BigNumber, providerUtils } from '@0x/utils';
import { Web3Wrapper } from '@0x/web3-wrapper';
import * as chai from 'chai';
import * as chaiAsPromised from 'chai-as-promised';
import * as ChaiBigNumber from 'chai-bignumber';
import * as dirtyChai from 'dirty-chai';

import { AbiGenDummyContract, artifacts, TestLibDummyContract } from '../src';

const txDefaults = {
    from: devConstants.TESTRPC_FIRST_ADDRESS,
    gas: devConstants.GAS_LIMIT,
};

const provider: Web3ProviderEngine = web3Factory.getRpcProvider({ shouldUseInProcessGanache: true });
const web3Wrapper = new Web3Wrapper(provider);

chai.config.includeStack = true;
chai.use(ChaiBigNumber());
chai.use(dirtyChai);
chai.use(chaiAsPromised);
const expect = chai.expect;
const blockchainLifecycle = new BlockchainLifecycle(web3Wrapper);

describe('AbiGenDummy Contract', () => {
    let abiGenDummy: AbiGenDummyContract;
    before(async () => {
        providerUtils.startProviderEngine(provider);
        abiGenDummy = await AbiGenDummyContract.deployFrom0xArtifactAsync(artifacts.AbiGenDummy, provider, txDefaults);
    });
    after(async () => {
        provider.stop();
    });
    beforeEach(async () => {
        await blockchainLifecycle.startAsync();
    });
    afterEach(async () => {
        await blockchainLifecycle.revertAsync();
    });

    describe('simplePureFunction', () => {
        it('should call simplePureFunction', async () => {
            const result = await abiGenDummy.simplePureFunction.callAsync();
            expect(result).bignumber.to.equal(new BigNumber(1));
        });
    });
    describe('simplePureFunctionWithInput', () => {
        it('should call simplePureFunctionWithInput', async () => {
            const result = await abiGenDummy.simplePureFunctionWithInput.callAsync(new BigNumber(5));
            expect(result).bignumber.to.equal(new BigNumber(6));
        });
    });
    describe('pureFunctionWithConstant', () => {
        it('should call pureFunctionWithConstant', async () => {
            const result = await abiGenDummy.pureFunctionWithConstant.callAsync();
            expect(result).bignumber.to.equal(new BigNumber(1234));
        });
    });
    describe('simpleRevert', () => {
        it('should call simpleRevert', async () => {
            return expectContractCallFailedAsync(abiGenDummy.simpleRevert.callAsync(), RevertReason.ValidatorError);
        });
    });
    describe('revertWithConstant', () => {
        it('should call revertWithConstant', async () => {
            return expectContractCallFailedAsync(
                abiGenDummy.revertWithConstant.callAsync(),
                RevertReason.ValidatorError,
            );
        });
    });
    describe('simpleRequire', () => {
        it('should call simpleRequire', async () => {
            return expectContractCallFailedAsync(abiGenDummy.simpleRequire.callAsync(), RevertReason.ValidatorError);
        });
    });
    describe('requireWithConstant', () => {
        it('should call requireWithConstant', async () => {
            return expectContractCallFailedAsync(
                abiGenDummy.requireWithConstant.callAsync(),
                RevertReason.ValidatorError,
            );
        });
    });
});

describe('Lib dummy contract', () => {
    let libDummy: TestLibDummyContract;
    before(async () => {
        await blockchainLifecycle.startAsync();
    });
    after(async () => {
        await blockchainLifecycle.revertAsync();
    });
    before(async () => {
        libDummy = await TestLibDummyContract.deployFrom0xArtifactAsync(artifacts.TestLibDummy, provider, txDefaults);
    });
    beforeEach(async () => {
        await blockchainLifecycle.startAsync();
    });
    afterEach(async () => {
        await blockchainLifecycle.revertAsync();
    });

    it('should call a library function', async () => {
        const result = await libDummy.publicAddOne.callAsync(new BigNumber(1));
        expect(result).bignumber.to.equal(new BigNumber(2));
    });

    it('should call a library function referencing a constant', async () => {
        const result = await libDummy.publicAddConstant.callAsync(new BigNumber(1));
        expect(result).bignumber.to.equal(new BigNumber(1235));
    });
});

// HACK (xianny): copied from @0x/contracts-test-utils to avoid circular dependency
/**
 * Resolves if the the contract call fails with the given revert reason.
 * @param p a Promise resulting from a contract call
 * @param reason a specific revert reason
 * @returns a new Promise which will reject if the conditions are not met and
 * otherwise resolve with no value.
 */
function expectContractCallFailedAsync<T>(p: Promise<T>, reason: RevertReason): Chai.PromisedAssertion {
    const rejectionMessageRegex = new RegExp(`^VM Exception while processing transaction: revert ${reason}$`);
    return expect(p).to.be.rejectedWith(rejectionMessageRegex);
}
