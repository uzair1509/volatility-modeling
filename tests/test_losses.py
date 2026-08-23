import numpy as np
import pytest
from volmodels.losses import mse, mae, qlike

#perfect forecast --> zero loss for all three
def test_zero_at_perfect_forecast():
  x = np.array([1.0, 2.0, 0.5, 4.0])
  assert mse(x, x) == pytest.approx(0)
  assert mae(x, x) == pytest.approx(0)
  assert qlike(x, x) == pytest.approx(0)

#loss can never be negative
def test_nonnegative():
  rng = np.random.default_rng(0)
  frc = rng.uniform(0.1, 5.0, 200)
  act = rng.uniform(0.1, 5.0, 200)
  assert mse(frc, act) >= 0
  assert mae(frc, act) >= 0
  assert qlike(frc, act) >= 0

#different lengths should fail loudly, not broadcast
def test_shape_mismatch_raises():
  with pytest.raises(ValueError):
    mse(np.ones(5), np.ones(4))
  with pytest.raises(ValueError):
    mae(np.ones(5), np.ones(4))
  with pytest.raises(ValueError):
    qlike(np.ones(5), np.ones(4))

#qlike punishes under-forecasting harder than over-forecasting
#this is why it can disagree with MSE about which model wins
def test_qlike_asymmetry():
  act = np.array([1.0])
  under = qlike(np.array([0.5]), act)
  over = qlike(np.array([2.0]), act)
  assert under > over
