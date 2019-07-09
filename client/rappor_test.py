

"""
rappor_test.py: Tests for rappor.py
"""
from io import StringIO
import copy
import math
import random
import unittest

import rappor  # module under test


class RapporParamsTest(unittest.TestCase):

  def setUp(self):
    self.typical_instance = rappor.Params()
    ti = self.typical_instance  # For convenience
    ti.num_cohorts = 64        # Number of cohorts
    ti.num_hashes = 2          # Number of bloom filter hashes
    ti.num_bloombits = 16      # Number of bloom filter bits
    ti.prob_p = 0.40           # Probability p
    ti.prob_q = 0.70           # Probability q
    ti.prob_f = 0.30           # Probability f

  def testFromCsv(self):
    f = io.StringIO('k,h,m,p,q,f\n32,2,64,0.5,0.75,0.6\n')
    params = rappor.Params.from_csv(f)
    self.assertEqual(32, params.num_bloombits)
    self.assertEqual(64, params.num_cohorts)

    # Malformed header
    f = cStringIO.StringIO('k,h,m,p,q\n32,2,64,0.5,0.75,0.6\n')
    self.assertRaises(rappor.Error, rappor.Params.from_csv, f)

    # Missing second row
    f = cStringIO.StringIO('k,h,m,p,q,f\n')
    self.assertRaises(rappor.Error, rappor.Params.from_csv, f)

    # Too many rows
    f = cStringIO.StringIO('k,h,m,p,q,f\n32,2,64,0.5,0.75,0.6\nextra')
    self.assertRaises(rappor.Error, rappor.Params.from_csv, f)

  def testGetBloomBits(self):
    for cohort in range(0, 64):
      b = rappor.get_bloom_bits('foo', cohort, 2, 16)
      #print 'cohort', cohort, 'bloom', b

  def testGetPrr(self):
    bloom = 1
    num_bits = 8
    for word in ('v1', 'v2', 'v3'):
      masks = rappor.get_prr_masks('secret', word, 0.5, num_bits)
      print ('masks'+ masks)

  def testToBigEndian(self):
    b = rappor.to_big_endian(1)
    print(repr(b))
    self.assertEqual(4, len(b))

  def testEncoder(self):
    # Test encoder with deterministic random function.
    params = copy.copy(self.typical_instance)
    params.prob_f = 0.5
    params.prob_p = 0.5
    params.prob_q = 0.75

    # return these 3 probabilities in sequence.
    rand = MockRandom([0.0, 0.6, 0.0], params)

    e = rappor.Encoder(params, 0, 'secret', rand)

    irr = e.encode("abc")

    self.assertEquals(64493, irr)  # given MockRandom, this is what we get


class MockRandom(object):
  """Returns one of three random values in a cyclic manner.

  Mock random function that involves *some* state, as needed for tests that
  call randomness several times. This makes it difficult to deal exclusively
  with stubs for testing purposes.
  """

  def __init__(self, cycle, params):
    self.p_gen = MockRandomCall(params.prob_p, cycle, params.num_bloombits)
    self.q_gen = MockRandomCall(params.prob_q, cycle, params.num_bloombits)

class MockRandomCall:
  def __init__(self, prob, cycle, num_bits):
    self.cycle = cycle
    self.n = len(self.cycle)
    self.prob = prob
    self.num_bits = num_bits

  def __call__(self):
    counter = 0
    r = 0
    for i in xrange(0, self.num_bits):
      rand_val = self.cycle[counter]
      counter += 1
      counter %= self.n  # wrap around
      r |= ((rand_val < self.prob) << i)
    return r


if __name__ == "__main__":
  unittest.main()
