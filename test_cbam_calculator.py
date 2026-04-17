import unittest

from cbam_calculator import (
    calculeaza_cbam,
    greutate_m2,
    greutate_panou_m2,
    obtine_valoare_implicita,
)


VALORI_ASTEPTATE_2026 = {
    ("Algeria", "7308"): 3.3000000000000003,
    ("Algeria", "7210"): 3.3220000000000005,
    ("Argentina", "7308"): 2.9480000000000004,
    ("Argentina", "7210"): 3.311,
    ("Australia", "7308"): 3.3000000000000003,
    ("Australia", "7210"): 3.5200000000000005,
    ("Azerbaijan", "7308"): 0.15400000000000003,
    ("Azerbaijan", "7210"): 2.079,
    ("Bosnia and Herzegovina", "7308"): 2.519,
    ("Bosnia and Herzegovina", "7210"): 3.1350000000000002,
    ("Brazil", "7308"): 1.903,
    ("Brazil", "7210"): 3.2010000000000005,
    ("Canada", "7308"): 1.6610000000000003,
    ("Canada", "7210"): 3.2010000000000005,
    ("Chile", "7308"): 2.255,
    ("Chile", "7210"): 2.7940000000000005,
    ("China", "7308"): 3.5255000000000005,
    ("China", "7210"): 6.6385000000000005,
    ("Colombia", "7308"): 3.1790000000000003,
    ("Colombia", "7210"): 3.9380000000000006,
    ("India", "7308"): 4.708000000000001,
    ("India", "7210"): 6.523000000000001,
    ("Indonesia", "7308"): 9.075000000000001,
    ("Indonesia", "7210"): 9.075000000000001,
    ("Iran", "7308"): 2.134,
    ("Iran", "7210"): 2.805,
    ("Japan", "7308"): 2.343,
    ("Japan", "7210"): 3.2450000000000006,
    ("Kazakhstan", "7308"): 5.896000000000001,
    ("Kazakhstan", "7210"): 5.896000000000001,
    ("Mexico", "7308"): 3.091,
    ("Mexico", "7210"): 3.2890000000000006,
    ("Myanmar_Burma", "7308"): 0.517,
    ("Myanmar_Burma", "7210"): 2.9700000000000006,
    ("New Zealand", "7308"): 2.6730000000000005,
    ("New Zealand", "7210"): 3.19,
    ("North Macedonia", "7308"): 1.6830000000000003,
    ("North Macedonia", "7210"): 2.959,
    ("Philippines", "7308"): 0.8140000000000001,
    ("Philippines", "7210"): 2.3980000000000006,
    ("Russia", "7308"): 3.9490000000000003,
    ("Russia", "7210"): 3.9490000000000003,
    ("Serbia", "7308"): 2.6510000000000002,
    ("Serbia", "7210"): 2.728,
    ("South Africa", "7308"): 4.642,
    ("South Africa", "7210"): 4.642,
    ("South Korea", "7308"): 2.3584000000000005,
    ("South Korea", "7210"): 4.2504,
    ("Taiwan", "7308"): 2.5663000000000005,
    ("Taiwan", "7210"): 2.6653000000000002,
    ("Thailand", "7308"): 2.5639035719,
    ("Thailand", "7210"): 4.718450000000001,
    ("Turcia", "7308"): 2.761,
    ("Turcia", "7210"): 6.072,
    ("Ukraine", "7308"): 2.797877632,
    ("Ukraine", "7210"): 3.7543,
    ("United Kingdom", "7308"): 2.75,
    ("United Kingdom", "7210"): 3.3440000000000003,
    ("United States", "7308"): 1.584,
    ("United States", "7210"): 3.19,
    ("Uzbekistan", "7308"): 3.531,
    ("Uzbekistan", "7210"): 3.311,
    ("Vietnam", "7308"): 2.607,
    ("Vietnam", "7210"): 3.124,
}


class TestCBAMCalculator(unittest.TestCase):
    def test_toate_valorile_2026_din_tabel_sunt_incarcate(self):
        for (tara, cod), valoare in VALORI_ASTEPTATE_2026.items():
            with self.subTest(tara=tara, cod=cod):
                self.assertEqual(obtine_valoare_implicita(tara, cod), (valoare, "specifica_tarii"))

    def test_greutate_m2_tabla_05_mm(self):
        self.assertAlmostEqual(greutate_m2(0.5), 3.925)

    def test_panou_sandwich_60_mm_turkiye(self):
        rezultat = calculeaza_cbam(
            tip_produs="panou_sandwich",
            grosime_panou_mm=60,
            suprafata_m2=500,
            tara="Turcia",
            cod_NC="7308",
            pret_ETS=80,
        )

        self.assertAlmostEqual(rezultat.greutate_kg_m2, 10.7)
        self.assertAlmostEqual(rezultat.greutate_tone, 5.35)
        self.assertAlmostEqual(rezultat.valoare_implicita, 2.761)
        self.assertEqual(rezultat.sursa_valoare_implicita, "specifica_tarii")
        self.assertAlmostEqual(rezultat.emisii_tco2, 14.77135)
        self.assertAlmostEqual(rezultat.cost_cbam_eur, 1181.708)
        self.assertAlmostEqual(rezultat.cost_cbam_eur_m2, 2.363416)

    def test_tabla_cutata_05_mm_china(self):
        rezultat = calculeaza_cbam(
            tip_produs="tabla_cutata",
            grosime_tabla_mm=0.5,
            suprafata_m2=300,
            tara="China",
            cod_NC="7210",
            pret_ETS=80,
        )

        self.assertAlmostEqual(rezultat.greutate_tone, 1.1775)
        self.assertAlmostEqual(rezultat.valoare_implicita, 6.6385000000000005)
        self.assertEqual(rezultat.sursa_valoare_implicita, "specifica_tarii")
        self.assertAlmostEqual(rezultat.emisii_tco2, 7.81683375)
        self.assertAlmostEqual(rezultat.cost_cbam_eur, 625.3467)

    def test_tara_cu_valoare_specifica_nu_foloseste_default(self):
        rezultat = calculeaza_cbam(
            tip_produs="tabla_cutata",
            grosime_tabla_mm=0.5,
            suprafata_m2=100,
            tara="United States",
            cod_NC="7210",
            pret_ETS=80,
        )

        self.assertAlmostEqual(rezultat.greutate_tone, 0.3925)
        self.assertAlmostEqual(rezultat.valoare_implicita, 3.19)
        self.assertEqual(rezultat.sursa_valoare_implicita, "specifica_tarii")
        self.assertAlmostEqual(rezultat.emisii_tco2, 1.252075)
        self.assertAlmostEqual(rezultat.cost_cbam_eur, 100.166)

    def test_tara_fara_valoare_specifica_foloseste_other_countries(self):
        rezultat = calculeaza_cbam(
            tip_produs="tabla_cutata",
            grosime_tabla_mm=0.5,
            suprafata_m2=100,
            tara="Nepal",
            cod_NC="7210",
            pret_ETS=80,
        )

        self.assertAlmostEqual(rezultat.greutate_tone, 0.3925)
        self.assertAlmostEqual(rezultat.valoare_implicita, 5.570235000000001)
        self.assertEqual(rezultat.sursa_valoare_implicita, "default_cod_nc")
        self.assertAlmostEqual(rezultat.emisii_tco2, 2.1863172375000004)
        self.assertAlmostEqual(rezultat.cost_cbam_eur, 174.90537900000003)

    def test_obtine_valoare_implicita_specifica_si_default(self):
        self.assertEqual(obtine_valoare_implicita("China", "7210"), (6.6385000000000005, "specifica_tarii"))
        self.assertEqual(obtine_valoare_implicita("Serbia", "7210"), (2.728, "specifica_tarii"))
        self.assertEqual(obtine_valoare_implicita("Myanmar_Burma", "7308"), (0.517, "specifica_tarii"))
        self.assertEqual(obtine_valoare_implicita("Nepal", "7210"), (5.570235000000001, "default_cod_nc"))

    def test_panou_sandwich_cu_table_exterior_interior_custom(self):
        greutate = greutate_panou_m2(
            grosime_panou_mm=60,
            grosime_tabla_exterior_mm=0.6,
            grosime_tabla_interior_mm=0.5,
        )
        self.assertAlmostEqual(greutate, 11.485)

        rezultat = calculeaza_cbam(
            tip_produs="panou_sandwich",
            grosime_panou_mm=60,
            grosime_tabla_exterior_mm=0.6,
            grosime_tabla_interior_mm=0.5,
            tip_panou="perete",
            suprafata_m2=500,
            tara="Turcia",
            cod_NC="7308",
            pret_ETS=80,
        )
        self.assertAlmostEqual(rezultat.greutate_kg_m2, 11.485)
        self.assertAlmostEqual(rezultat.greutate_tone, 5.7425)

    def test_panou_acoperis_este_mai_greu_decat_panou_perete(self):
        perete = greutate_panou_m2(
            grosime_panou_mm=60,
            grosime_tabla_exterior_mm=0.5,
            grosime_tabla_interior_mm=0.5,
            tip_panou="perete",
        )
        acoperis = greutate_panou_m2(
            grosime_panou_mm=60,
            grosime_tabla_exterior_mm=0.5,
            grosime_tabla_interior_mm=0.5,
            tip_panou="acoperis",
        )

        self.assertAlmostEqual(perete, 10.7)
        self.assertAlmostEqual(acoperis, 11.014)
        self.assertGreater(acoperis, perete)


if __name__ == "__main__":
    unittest.main()
