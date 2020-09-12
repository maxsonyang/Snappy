import unittest
from Block import *
from SnapBlocks import *
from Project import *
from math import pi

class TestBlock(unittest.TestCase):

	def test_xmltoblock(self):
		testXMLString = '''
		<block s="reportSum">
			<l>1</l>
			<l></l>
		</block>
		'''
		testBlock = xmlToBlock(testXMLString)
		self.assertEqual(testBlock.signature, 'reportSum')
		self.assertEqual(testBlock.inputs, [1, None])

	def test_listxmltoblock(self):
		testXMLString = '''
		<block s="reportSum">
			<l>1</l>
			<block s="reportNewList">
				<list>
					<l>2.2</l>
					<block s="reportNewList">
						<list>
							<l>3</l>
							<l>4</l>
						</list>
					</block>
				</list>
			</block>
		</block>
		'''
		testBlock = xmlToBlock(testXMLString)
		self.assertEqual(testBlock.inputs, [1, [2.2, [3, 4]]])

	def test_blocktoxml(self):
		testBlock = Block('reportSum', [1, 2])
		testXMLString = blockToXML(testBlock)
		expectedOutput = '<block s="reportSum"><l>1</l><l>2</l></block>'
		self.assertEqual(testXMLString, expectedOutput)

	def test_listblocktoxml(self):
		testBlock = Block('reportSum', [1, [2.2, [3, 4]]])
		testXMLString = blockToXML(testBlock)
		expectedOutput = '''
		<block s="reportSum"><l>1</l>
			<block s="reportNewList">
				<list>
					<l>2.2</l>
					<block s="reportNewList">
						<list>
							<l>3</l>
							<l>4</l>
						</list>
					</block>
					</list>
				</block>
		</block>
		'''.replace('\t', '').replace('\n', '')
		self.assertEqual(testXMLString, expectedOutput)

class TestExecutor(unittest.TestCase):

	def test_evaluateValue(self):
		'''
		Simple tests to ensure that hardcoded values
		are being evaluated properly.
		'''
		p = Project()
		e = p.executor

		# Check Int Type
		self.assertEqual(e.evaluate(2), 2)

		# Check float
		self.assertEqual(e.evaluate(2.2), 2.2)

		# Check string
		self.assertEqual(e.evaluate('two'), 'two')

		# Check List
		self.assertEqual(e.evaluate([1, 2, 3]), [1, 2, 3])
	
	def test_operators(self):

		p = Project()
		e = p.executor

		# Check addition operator
		self.assertEqual(e.evaluate(plus(1, 2)), 3)
		# Check subtraction operator
		self.assertEqual(e.evaluate(subtract(0, 1)), -1)
		# Check multiply operator
		self.assertEqual(e.evaluate(multiply(5, 5)), 25)
		# Check division operator
		self.assertEqual(e.evaluate(divide(20, 2)), 10)
		# Check power operator
		self.assertEqual(e.evaluate(power(7, 2)), 49)
		# Check modulo operator
		self.assertEqual(e.evaluate(modulo(7, 2)), 1)
		# Check round operator
		self.assertEqual(e.evaluate(reportRound(2.51)), 3)
		# Check absolute value
		self.assertEqual(e.evaluate(absOf(-10)), 10)
		self.assertEqual(e.evaluate(absOf(5)), 5)
		# Check negation
		self.assertEqual(e.evaluate(negOf(10)), -10)
		self.assertEqual(e.evaluate(negOf(-5)), 5)
		# Check ceil operator
		self.assertEqual(e.evaluate(ceilOf(2.1)), 3)
		# Check floor operator
		self.assertEqual(e.evaluate(floorOf(2.9)), 2)
		# Check square root operator
		self.assertEqual(e.evaluate(sqrtOf(9)), 3)
		# Sin operator
		self.assertAlmostEqual(e.evaluate(sinOf(pi)), 0, delta=0.001)
		# cos operator
		self.assertAlmostEqual(e.evaluate(cosOf(pi)), -1, delta=0.001)
		# tan operator
		self.assertAlmostEqual(e.evaluate(tanOf(pi)), 0, delta=0.001)
		# asin operator
		self.assertAlmostEqual(e.evaluate(asinOf(1)), pi / 2, delta=0.001)
		# acos operator
		self.assertAlmostEqual(e.evaluate(acosOf(1)), 0, delta=0.001)
		# atan operator
		self.assertAlmostEqual(e.evaluate(atanOf(1)), pi / 4, delta=0.001)
		# natural logarithm operator
		self.assertAlmostEqual(e.evaluate(lnOf(4)), 1.386, delta=0.001)
		# log10 operator
		self.assertEqual(e.evaluate(logOf(10)), 1)
		# binary log oeprator
		self.assertEqual(e.evaluate(binLogOf(4)), 2)
		# e power operator
		self.assertAlmostEqual(e.evaluate(eTo(2)), 7.3891, 3)
		# ten power operator
		self.assertEqual(e.evaluate(tenTo(4)), 10000)
		# two power operator
		self.assertEqual(e.evaluate(twoTo(4)), 16)
		# identity operator
		self.assertEqual(e.evaluate(identity(1)), 1)
		# random operator
		self.assertIn(e.evaluate(pickRandom(1, 10)), [_ for _ in range(1, 11)])
		# less than operator
		self.assertTrue(e.evaluate(lessThan(1, 2)))
		self.assertFalse(e.evaluate(lessThan(2, 1)))
		# equal to operator
		self.assertTrue(e.evaluate(equalTo(1, 1)))
		self.assertFalse(e.evaluate(equalTo(40, 41)))
		# greater than operator
		self.assertTrue(e.evaluate(greaterThan(4, 3)))
		self.assertFalse(e.evaluate(greaterThan(3, 4)))
		# and operator
		self.assertTrue(e.evaluate(andOp(True, True)))
		self.assertFalse(e.evaluate(andOp(False, True)))
		# or operator
		self.assertTrue(e.evaluate(orOp(False, True)))
		self.assertFalse(e.evaluate(orOp(False, False)))
		# not operator
		self.assertTrue(e.evaluate(notOp(False)))
		self.assertFalse(e.evaluate(notOp(True)))
		# Boolean value operators
		self.assertTrue(e.evaluate(boolean(True)))
		self.assertFalse(e.evaluate(boolean(False)))
		self.assertTrue(e.evaluate(boolean(1)))
		self.assertFalse(e.evaluate(boolean(0)))
		# join operator
		self.assertEqual(e.evaluate(join(['this', 'is', 'a', 'test'])), 'thisisatest')
		# text split operator
		self.assertEqual(e.evaluate(textSplit('this is a test', ' ')), ['this', 'is', 'a', 'test'])
		self.assertEqual(e.evaluate(textSplit('atestbtestctestd', 'test')), ['a', 'b', 'c', 'd'])

	def test_global_variables(self):

		p = Project()
		p.addGlobalVariable('testVariable')
		p.executor.execute(setVariableTo('testVariable', 12))
		p.executor.evaluate(Variable('testVariable'))

	def test_local_variables(self):
		
		p = Project()
		localScope = {}

		# Set up the initial test values in global and local scope.
		p.addGlobalVariable('testVariable')
		p.executor.execute(setVariableTo('testVariable', 'global'), localScope)
		p.executor.execute(scriptVariables(['testVariable']), localScope)
		p.executor.execute(setVariableTo('testVariable', 'local'), localScope)

		# Check the value with and without the local scope.
		self.assertEqual(p.executor.evaluate(Variable('testVariable')), 'global')
		self.assertEqual(p.executor.evaluate(Variable('testVariable'), localScope), 'local')

	def test_change_var(self):

		p = Project()
		localScope = {}

		# Set up the variables
		p.addGlobalVariable('testVariable')
		p.executor.execute(setVariableTo('testVariable', 0), localScope)
		p.executor.execute(scriptVariables(['testVariable']), localScope)
		p.executor.execute(setVariableTo('testVariable', 12), localScope)

		p.executor.execute(changeVariableBy('testVariable', 5))
		p.executor.execute(changeVariableBy('testVariable', .12), localScope)

		self.assertEqual(p.executor.evaluate(Variable('testVariable')), 5)
		self.assertEqual(p.executor.evaluate(Variable('testVariable'), localScope), 12.12)
		

if __name__ == '__main__':
	unittest.main()
